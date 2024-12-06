from setuptools import setup, find_packages

setup(
    name='criteria',
    version='0.1.1',
    description='Deep learning loss functions and models for image similarity',
    author='Minh-Ha Le',
    author_email='minhha.x89@gmail.com',
    packages=find_packages(exclude=['outputs', '__pycache__', 'outputs.*', '__pycache__.*']),
    install_requires=[
        'torch',
        'gdown',
        'numpy',
        'hydra-core',
        'omegaconf',
        'openai-clip',
        'torchvision>=0.2.1,<0.20.0',
        'pillow>=8.3.2,<10.1.0',
        'scipy>=1.0.1,<1.11.0',
        'absl-py',
        'google-auth-oauthlib<1.1,>=0.5',
        'grpcio',
        'tensorboard-data-server'
    ],
    python_requires='>=3.6',
)