from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="mathwork",
        version="1.8",
        description="The great package.",
        author="unknown",
        packages=["mathwork"],
        install_requires=[
            'tensorflow', 'pandas', 'scikit-learn', 'torch', 'opencv-python',
            'pillow', 'scikit-image', 'numpy', 'scipy',
            'matplotlib', 'pywavelets', 'seaborn', 'torchvision', 'torchaudio',
            'keras', 'transformers', 'tqdm', 'ultralytics'
        ],
        dependency_links=[
            'git+https://github.com/facebookresearch/detectron2.git#egg=detectron2'
        ],
        package_data={
        'mathwork': [
            'Lab Tasks/*',  
            'Lab Manuals/*', 
        ]},
        zip_safe=False,
    )
