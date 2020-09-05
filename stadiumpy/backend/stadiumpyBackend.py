import os, glob, yaml
import stadiumpy as stdpy

# read inputYAML
inp_file_yaml = os.path.join(stdpy.__path__[0], 'backend', 'input_file.yaml')
adv_prf_yaml = os.path.join(stdpy.__path__[0], 'backend', 'advRFparam.yaml')
descrip_yaml = os.path.join(stdpy.__path__[0], 'backend', 'description.yaml')
direc_yaml = os.path.join(stdpy.__path__[0], 'backend', 'directories_names.yaml')

## User defined
USER_adv_prf_yaml = os.path.join(stdpy.__path__[0], 'backend', 'USER_advRFparam.yaml')
USER_inp_yaml = os.path.join(stdpy.__path__[0], 'backend', 'USER_input_file.yaml')
USER_direc_yaml = os.path.join(stdpy.__path__[0], 'backend', 'USER_directories_names.yaml')
print("Hello from ", __name__)
def main():
    with open(inp_file_yaml) as f:
        inp = yaml.load(f, Loader=yaml.FullLoader)

    with open(adv_prf_yaml) as f:
        adv_prf = yaml.load(f, Loader=yaml.FullLoader)

    with open(descrip_yaml) as f:
        stdpydesc = yaml.load(f, Loader=yaml.FullLoader)

    with open(USER_inp_yaml) as f:
        user_inp = yaml.load(f, Loader=yaml.FullLoader)

    with open(direc_yaml) as f:
        direcDict = yaml.load(f, Loader=yaml.FullLoader)

if __name__ == '__main__':
    main()

