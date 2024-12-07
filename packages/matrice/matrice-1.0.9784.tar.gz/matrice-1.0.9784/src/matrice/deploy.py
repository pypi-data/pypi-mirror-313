import os
import threading
import time
import urllib.request
import requests
import uvicorn
from fastapi import Body, FastAPI, File, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from io import BytesIO
from PIL import Image, ImageDraw
import logging

from .actionTracker import ActionTracker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MatriceDeploy:
    """
    A class for deploying ML models as REST APIs using FastAPI.
    
    This class handles model loading, inference, monitoring and automatic shutdown
    of idle deployments.
    """

    def __init__(self, load_model, predict, action_id, port):
        self.action_id = action_id
        self.actionTracker = ActionTracker(action_id)
        self.rpc = self.actionTracker.session.rpc

        self.action_details = self.actionTracker.action_details
        logger.info(f"Action details: {self.action_details}")

        # Extract deployment details
        self._idDeploymentInstance = self.action_details["_idModelDeployInstance"]
        self._idDeployment = self.action_details["_idDeployment"]
        self.model_id = self.action_details["_idModelDeploy"]

        # Store model functions
        self.load_model = lambda actionTracker: load_model(actionTracker)
        self.predict = lambda model, image: predict(model, image)

        # Initialize model and monitoring variables
        self.model = None
        self.last_no_inference_time = -1
        self.shutdown_on_idle_threshold = int(self.action_details["shutdownThreshold"]) * 60
        
        # Setup FastAPI app
        self.app = FastAPI()
        self.ip = self.get_ip()
        self.port = int(port)
        
        # Initialize performance tracking
        self.load_time = None
        self.prediction_time_ms = []
        self.min_inference_time_ms = float('inf')

        # Start monitoring thread
        self.run_shutdown_checker()

        # Register API endpoints
        self._register_endpoints()

    def _register_endpoints(self):
        @self.app.post("/inference/")
        async def serve_inference(image: UploadFile = File(...)):
            image_data = await image.read()
            results, ok = self.inference(image_data)

            if ok:
                return JSONResponse(content=jsonable_encoder({
                    "status": 1,
                    "message": "Request success",
                    "result": results
                }))
            else:
                raise HTTPException(status_code=500, detail="Inference failed")

        @self.app.post("/inference_from_url/")
        async def serve_inference_from_url(imageUrl: str = Body(embed=True)):
            if not imageUrl:
                raise HTTPException(status_code=400, detail="Please provide imageUrl")

            try:
                response = requests.get(imageUrl, timeout=10)
                response.raise_for_status()
                image_data = response.content
            except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=400, detail=f"Failed to fetch image: {str(e)}")

            results, ok = self.inference(image_data)

            if ok:
                return JSONResponse(content=jsonable_encoder({
                    "status": 1,
                    "message": "Request success", 
                    "result": results
                }))
            else:
                raise HTTPException(status_code=500, detail="Inference failed")

    def start_server(self):
        """Start the FastAPI server"""
        host = "0.0.0.0"
        port = 80
        self.update_deployment_address()
        
        try:
            self.warmup()
            self.actionTracker.update_status("MDL_DPL_STR", "OK", "Model deployment started")
            uvicorn.run(self.app, host=host, port=port)
        except Exception as e:
            logger.error(f"Failed to start server: {str(e)}")
            self.actionTracker.update_status("ERROR", "ERROR", f"Model deployment error: {str(e)}")

    def warmup(self):
        """Perform model warmup by running test inferences"""
        try:    
            logger.info("Starting model warmup...")
            for i in range(10):
                self.inference(self.create_image_bytes())
            self.prediction_time_ms = []
            logger.info("Model warmup completed successfully")
        except Exception as e:
            logger.error(f"Error during warmup: {str(e)}")
            raise

    def create_image_bytes(self):
        """
        Creates a test image in memory for warmup.
        
        Returns
        -------
        bytes
            JPEG image data
        """
        image = Image.new("RGB", (224, 224), color="blue")
        draw = ImageDraw.Draw(image)
        draw.text((50, 100), "Test", fill="white")
        
        image_bytes_io = BytesIO()
        image.save(image_bytes_io, format="JPEG")
        image_bytes_io.seek(0)
        return image_bytes_io.read()
    
    def get_ip(self):
        """Get the public IP address of the deployment"""
        try:
            external_ip = urllib.request.urlopen("https://ident.me", timeout=5).read().decode("utf8")
            logger.info(f"Public IP address: {external_ip}")
            return external_ip
        except Exception as e:
            logger.error(f"Failed to get public IP: {str(e)}")
            raise

    def inference(self, image):
        """
        Run model inference on input image
        
        Parameters
        ----------
        image : bytes
            Input image data
            
        Returns
        -------
        tuple
            (results, success_flag)
        """
        now = time.time()
        
        # Lazy load model on first inference
        if self.model is None:
            self.model = self.load_model(self.actionTracker)
            self.load_time = time.time() - now
            now = time.time()

        self.last_no_inference_time = -1

        try:
            results = self.predict(self.model, image)
            inference_time = (time.time() - now) * 1000
            self.min_inference_time_ms = min(self.min_inference_time_ms, inference_time)
            self.prediction_time_ms.append(inference_time)
            return results, True
        except Exception as e:
            logger.error(f"Inference error: {str(e)}")
            return None, False

    def trigger_shutdown_if_needed(self):
        """Check idle time and trigger shutdown if threshold exceeded"""
        if self.last_no_inference_time == -1:
            self.last_no_inference_time = time.time()
            return
            
        elapsed_time = time.time() - self.last_no_inference_time
        if elapsed_time > self.shutdown_on_idle_threshold:
            try:
                self.actionTracker.save_benchmark_results(self.min_inference_time_ms, batch_size=1)
                logger.info("Shutting down due to idle time exceeding threshold")
                
                self.rpc.delete(f"/v1/deployment/delete_deploy_instance/{self._idDeploymentInstance}")
                self.actionTracker.update_status("MDL_DPL_STP", "SUCCESS", "Model deployment stopped")
                
                time.sleep(10)
                os._exit(0)
            except Exception as e:
                logger.error(f"Error during shutdown: {str(e)}")
                os._exit(1)
        else:
            logger.info(f"Time since last inference: {elapsed_time:.1f}s")
            logger.info(f"Time until shutdown: {self.shutdown_on_idle_threshold - elapsed_time:.1f}s")

    def shutdown_checker(self):
        """Background thread to check for idle shutdown"""
        while True:
            try:
                self.trigger_shutdown_if_needed()
            except Exception as e:
                logger.error(f"Error in shutdown checker: {str(e)}")
            time.sleep(10)

    def run_shutdown_checker(self):
        """Start the shutdown checker thread"""
        checker_thread = threading.Thread(target=self.shutdown_checker, daemon=True)
        checker_thread.start()

    def update_deployment_address(self):
        """Update the deployment address in the backend"""
        ip = self.get_ip()
        port = self.port

        payload = {
            "port": port,
            "ipAddress": ip,
            "_idDeploymentInstance": self._idDeploymentInstance,
            "_idModelDeploy": self._idDeployment,
        }

        try:
            self.rpc.put(path="/v1/deployment/update_deploy_instance_address", payload=payload)
            logger.info(f"Updated deployment address to {ip}:{port}")
        except Exception as e:
            logger.error(f"Failed to update deployment address: {str(e)}")
            raise
