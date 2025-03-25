from setuptools import setup, find_packages

setup(
    name="lunar_lander",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pygame>=2.5.0",
        "Box2D>=2.4.1",
        "numpy>=1.24.0",
        "stable-baselines3>=2.1.0",
        "gymnasium>=0.29.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=0.900",
        ],
    },
    author="[Your Name]",
    author_email="[Your Email]",
    description="A custom Lunar Lander environment for reinforcement learning",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/[your-username]/lunar-lander",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
) 