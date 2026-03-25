#!/usr/bin/env python3
"""
Wan Animate Installation and Setup Script
Based on: https://wanimate.net/#installation

This script automates the installation process for Wan2.2 Wan Animate framework
including cloning the repository, installing dependencies, downloading model weights,
and running demos.
"""

import os
import subprocess
import sys
from pathlib import Path
import argparse
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WanAnimateInstaller:
    """Installer for Wan Animate framework"""
    
    # Available models
    MODELS = {
        't2v': {
            'name': 'T2V-A14B',
            'description': 'Text-to-Video MoE model, supports 480P & 720P',
            'size': '~14B parameters',
            'huggingface': 'Wan-AI/Wan2.2-T2V-A14B'
        },
        'i2v': {
            'name': 'I2V-A14B',
            'description': 'Image-to-Video MoE model, supports 480P & 720P',
            'size': '~14B parameters',
            'huggingface': 'Wan-AI/Wan2.2-I2V-A14B'
        },
        'ti2v': {
            'name': 'TI2V-5B',
            'description': 'High-compression VAE, T2V+I2V, supports 720P',
            'size': '~5B parameters',
            'huggingface': 'Wan-AI/Wan2.2-TI2V-5B'
        },
        's2v': {
            'name': 'S2V-14B',
            'description': 'Speech-to-Video model, supports 480P & 720P',
            'size': '~14B parameters',
            'huggingface': 'Wan-AI/Wan2.2-S2V-14B'
        },
        'animate': {
            'name': 'Animate-14B',
            'description': 'Character animation and replacement',
            'size': '~14B parameters',
            'huggingface': 'Wan-AI/Wan2.2-Animate-14B'
        }
    }
    
    def __init__(self, base_path: str = None):
        """Initialize the installer
        
        Args:
            base_path: Base directory for installation (default: current directory)
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.wan_dir = self.base_path / "Wan2.2"
        
    def clone_repository(self) -> bool:
        """Step 1: Clone the Wan2.2 repository"""
        logger.info("Step 1: Cloning Wan2.2 repository...")
        logger.info(f"Repository will be cloned to: {self.wan_dir}")
        
        try:
            if self.wan_dir.exists():
                logger.warning(f"Directory {self.wan_dir} already exists. Skipping clone.")
                return True
            
            os.chdir(self.base_path)
            cmd = ["git", "clone", "https://github.com/Wan-Video/Wan2.2.git"]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info("✓ Repository cloned successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Failed to clone repository: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"✗ Unexpected error during clone: {e}")
            return False
    
    def install_dependencies(self) -> bool:
        """Step 2: Install Python dependencies"""
        logger.info("Step 2: Installing dependencies...")
        
        try:
            if not self.wan_dir.exists():
                logger.error("Wan2.2 directory not found. Please clone repository first.")
                return False
            
            os.chdir(self.wan_dir)
            
            # Check Python version
            if sys.version_info < (3, 8):
                logger.error("Python 3.8 or higher is required")
                return False
            
            # Install requirements
            logger.info("Installing base requirements...")
            cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
            subprocess.run(cmd, check=True)
            
            # Ensure torch >= 2.4.0
            logger.info("Ensuring torch >= 2.4.0...")
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "torch>=2.4.0"]
            subprocess.run(cmd, check=True)
            
            # Try installing flash_attn
            logger.info("Installing flash_attn (may take a while)...")
            cmd = [sys.executable, "-m", "pip", "install", "flash_attn"]
            try:
                subprocess.run(cmd, check=True)
                logger.info("✓ flash_attn installed successfully")
            except subprocess.CalledProcessError:
                logger.warning("⚠ flash_attn installation failed - this is optional")
            
            logger.info("✓ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Failed to install dependencies: {e}")
            return False
        except Exception as e:
            logger.error(f"✗ Unexpected error during installation: {e}")
            return False
    
    def install_s2v_dependencies(self) -> bool:
        """Install optional Speech-to-Video dependencies"""
        logger.info("Installing Speech-to-Video (CosyVoice) dependencies...")
        
        try:
            os.chdir(self.wan_dir)
            req_file = self.wan_dir / "requirements_s2v.txt"
            
            if not req_file.exists():
                logger.warning("requirements_s2v.txt not found")
                return False
            
            cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements_s2v.txt"]
            subprocess.run(cmd, check=True)
            logger.info("✓ S2V dependencies installed successfully")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to install S2V dependencies: {e}")
            return False
    
    def download_models(self, models: list = None, use_modelscope: bool = False) -> bool:
        """Step 3: Download model weights
        
        Args:
            models: List of models to download ('t2v', 'i2v', 'ti2v', 's2v', 'animate')
            use_modelscope: Use ModelScope instead of HuggingFace (for China regions)
        """
        logger.info("Step 3: Downloading model weights...")
        
        if not models:
            models = ['t2v']
        
        # Filter valid models
        models = [m for m in models if m in self.MODELS]
        
        if not models:
            logger.error("No valid models specified")
            return False
        
        try:
            os.chdir(self.wan_dir)
            
            if use_modelscope:
                return self._download_with_modelscope(models)
            else:
                return self._download_with_huggingface(models)
        except Exception as e:
            logger.error(f"✗ Error downloading models: {e}")
            return False
    
    def _download_with_huggingface(self, models: list) -> bool:
        """Download models using HuggingFace"""
        logger.info("Installing huggingface-cli...")
        try:
            cmd = [sys.executable, "-m", "pip", "install", "huggingface_hub[cli]"]
            subprocess.run(cmd, check=True, capture_output=True)
            
            for model_key in models:
                model = self.MODELS[model_key]
                logger.info(f"Downloading {model['name']}...")
                
                cmd = [
                    "huggingface-cli", "download",
                    model['huggingface'],
                    "--local-dir", f"./{model['name']}"
                ]
                subprocess.run(cmd, check=True)
                logger.info(f"✓ {model['name']} downloaded")
            
            return True
        except Exception as e:
            logger.error(f"✗ HuggingFace download failed: {e}")
            return False
    
    def _download_with_modelscope(self, models: list) -> bool:
        """Download models using ModelScope (for China regions)"""
        logger.info("Installing modelscope...")
        try:
            cmd = [sys.executable, "-m", "pip", "install", "modelscope"]
            subprocess.run(cmd, check=True, capture_output=True)
            
            for model_key in models:
                model = self.MODELS[model_key]
                logger.info(f"Downloading {model['name']} from ModelScope...")
                
                modelscope_id = model['huggingface'].replace('Wan-AI/', 'Wan-AI/')
                cmd = [
                    "modelscope", "download",
                    modelscope_id,
                    "--local_dir", f"./{model['name']}"
                ]
                subprocess.run(cmd, check=True)
                logger.info(f"✓ {model['name']} downloaded")
            
            return True
        except Exception as e:
            logger.error(f"✗ ModelScope download failed: {e}")
            return False
    
    def print_system_requirements(self):
        """Print system requirements"""
        logger.info("\n" + "="*60)
        logger.info("SYSTEM REQUIREMENTS")
        logger.info("="*60)
        logger.info("GPU with 8GB+ VRAM recommended")
        logger.info("Python 3.8 or higher")
        logger.info("CUDA 11.8 or compatible")
        logger.info("16GB+ RAM recommended")
        logger.info("="*60 + "\n")
    
    def print_available_models(self):
        """Print available models"""
        logger.info("\n" + "="*60)
        logger.info("AVAILABLE MODELS")
        logger.info("="*60)
        for key, model in self.MODELS.items():
            logger.info(f"\n{model['name']} ({key})")
            logger.info(f"  Description: {model['description']}")
            logger.info(f"  Size: {model['size']}")
            logger.info(f"  HuggingFace: {model['huggingface']}")
        logger.info("="*60 + "\n")
    
    def print_quick_reference(self):
        """Print quick reference commands"""
        logger.info("\n" + "="*60)
        logger.info("QUICK REFERENCE: RUN WAN2.2")
        logger.info("="*60)
        
        examples = {
            'T2V': 'python generate.py --task t2v-A14B --size 1280*720 --ckpt_dir ./Wan2.2-T2V-A14B --offload_model True --convert_model_dtype --prompt "Your prompt here"',
            'I2V': 'python generate.py --task i2v-A14B --size 1280*720 --ckpt_dir ./Wan2.2-I2V-A14B --offload_model True --convert_model_dtype --image examples/i2v_input.JPG --prompt "Your prompt here"',
            'TI2V': 'python generate.py --task ti2v-5B --size 1280*704 --ckpt_dir ./Wan2.2-TI2V-5B --offload_model True --convert_model_dtype --t5_cpu --prompt "Your prompt here"',
            'S2V': 'python generate.py --task s2v-14B --size 1024*704 --ckpt_dir ./Wan2.2-S2V-14B/ --offload_model True --convert_model_dtype --prompt "Your prompt here" --audio examples/talk.wav',
            'Character Animation': 'python ./wan/modules/animate/preprocess/preprocess_data.py --ckpt_path ./Wan2.2-Animate-14B/process_checkpoint --video_path ./examples/wan_animate/animate/video.mp4 --refer_path ./examples/wan_animate/animate/image.jpeg --save_path ./examples/wan_animate/animate/process_results --resolution_area 1280 720 --retarget_flag --use_flux',
        }
        
        for task, cmd in examples.items():
            logger.info(f"\n{task}:")
            logger.info(f"  {cmd}")
        
        logger.info("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Wan Animate Installation and Setup',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full installation with all defaults
  python wan_animate_setup.py

  # Clone only
  python wan_animate_setup.py --clone-only

  # Install dependencies only
  python wan_animate_setup.py --install-deps-only

  # Download specific models
  python wan_animate_setup.py --models t2v i2v animate

  # Download models using ModelScope (China)
  python wan_animate_setup.py --models t2v --use-modelscope

  # Print available models
  python wan_animate_setup.py --list-models
        """
    )
    
    parser.add_argument(
        '--base-path',
        default=None,
        help='Base installation directory (default: current directory)'
    )
    parser.add_argument(
        '--clone-only',
        action='store_true',
        help='Only clone the repository'
    )
    parser.add_argument(
        '--install-deps-only',
        action='store_true',
        help='Only install dependencies'
    )
    parser.add_argument(
        '--models',
        nargs='+',
        default=['t2v'],
        help='Models to download: t2v, i2v, ti2v, s2v, animate'
    )
    parser.add_argument(
        '--use-modelscope',
        action='store_true',
        help='Use ModelScope for model downloads (for China regions)'
    )
    parser.add_argument(
        '--install-s2v',
        action='store_true',
        help='Install Speech-to-Video dependencies'
    )
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='List available models'
    )
    parser.add_argument(
        '--skip-models',
        action='store_true',
        help='Skip model downloading'
    )
    
    args = parser.parse_args()
    
    installer = WanAnimateInstaller(args.base_path)
    
    # Print system requirements
    installer.print_system_requirements()
    
    # List models if requested
    if args.list_models:
        installer.print_available_models()
        return 0
    
    # Step 1: Clone repository
    if not args.install_deps_only:
        if not installer.clone_repository():
            logger.error("Installation aborted")
            return 1
    
    if args.clone_only:
        logger.info("Clone completed. Use without --clone-only to continue with full setup.")
        return 0
    
    # Step 2: Install dependencies
    if not args.clone_only:
        if not installer.install_dependencies():
            logger.error("Installation aborted")
            return 1
        
        if args.install_s2v:
            installer.install_s2v_dependencies()
    
    # Step 3: Download models
    if not args.skip_models:
        if not installer.download_models(
            models=args.models,
            use_modelscope=args.use_modelscope
        ):
            logger.error("Model download failed")
            return 1
    
    # Print quick reference
    installer.print_quick_reference()
    
    logger.info("✓ Installation completed successfully!")
    logger.info(f"✓ Wan2.2 is ready at: {installer.wan_dir}")
    logger.info("✓ You can now run: python generate.py --task <task> --ckpt_dir <model_path>")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
