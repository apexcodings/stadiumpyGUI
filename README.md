
## Installation Steps

- Create Environment
`conda create -n stadiumpy python=3.7`

- Activate Environment and install packages
`conda install -c conda-forge obspy=1.1.0`
`conda install -c conda-forge pygmt=0.1.2=py37hc8dfbb8_0`
`conda install -c conda-forge shapely=1.7.0=py37hfcf0db4_3`
`conda install -c conda-forge cartopy=0.18.0=py37h08e9697_0`
`conda install -c conda-forge fortran-compiler`
`pip install obspyh5`
`conda install -c conda-forge tqdm=4.48.2=pyh9f0ad1d_0`
`pip install rf`
`pip install splitwavepy`

### Export environment
`conda env export --name stadiumpy > stadiumpy_env.yml`