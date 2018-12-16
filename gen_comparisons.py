import subprocess
from time import sleep

from templates import pbrt_template, nori_template

# print(nori_template)

test_cases = {
    "SSS" : {
        "color" : [ 0.917647059, 0.752941176, 0.525490196 ],
        "metallic" : [ 0 ],
        "roughness" : [ 0.1 ],
        "sheen" : [ 0 ],
        "sheentint" : [ 0 ],
        "clearcoat" : [ 0 ],
        "clearcoatgloss" : [ 0 ],
        "speculartint" : [ 0 ],
        "anisotropic" : [ 0 ],
        "eta" : [ 1.5 ],
        "spectrans" : [ 0.9 ],
        "scatterdistance" : [ 1, 0.5, 0.5 ],
    },
    "metallic" : {
        "color" : [ 0.917647059, 0.752941176, 0.525490196 ],
        "metallic" : [ 1 ],
        "roughness" : [ 0.3 ],
        "sheen" : [ 0 ],
        "sheentint" : [ 0 ],
        "clearcoat" : [ 0 ],
        "clearcoatgloss" : [ 0 ],
        "speculartint" : [ 0 ],
        "anisotropic" : [ 0 ],
        "eta" : [ 1.5 ],
        "spectrans" : [ 0 ],
        "scatterdistance" : [ 0, 0, 0 ],
    },
    "diffuse" : {
        "color" : [ 0.42, 0.8, 0.66 ],
        "metallic" : [ 0 ],
        "roughness" : [ 0 ],
        "sheen" : [ 0 ],
        "sheentint" : [ 0 ],
        "clearcoat" : [ 0 ],
        "clearcoatgloss" : [ 0 ],
        "speculartint" : [ 0 ],
        "anisotropic" : [ 0 ],
        "eta" : [ 1.5 ],
        "spectrans" : [ 0 ],
        "scatterdistance" : [ 0, 0, 0 ],
    },
    "diffuse_sheen" : {
        "color" : [ 0.42, 0.8, 0.66 ],
        "metallic" : [ 0 ],
        "roughness" : [ 0 ],
        "sheen" : [ 1 ],
        "sheentint" : [ 1 ],
        "clearcoat" : [ 0 ],
        "clearcoatgloss" : [ 0 ],
        "speculartint" : [ 0 ],
        "anisotropic" : [ 0 ],
        "eta" : [ 1.5 ],
        "spectrans" : [ 0 ],
        "scatterdistance" : [ 0, 0, 0 ],
    },
    "diffuse_clearcoat" : {
        "color" : [ 0.42, 0.8, 0.66 ],
        "metallic" : [ 0 ],
        "roughness" : [ 0 ],
        "sheen" : [ 0 ],
        "sheentint" : [ 0 ],
        "clearcoat" : [ 1 ],
        "clearcoatgloss" : [ 0.7 ],
        "speculartint" : [ 0 ],
        "anisotropic" : [ 0 ],
        "eta" : [ 1.5 ],
        "spectrans" : [ 0 ],
        "scatterdistance" : [ 0, 0, 0 ],
    },
    "transmission_pure" : {
        "color" : [ 0.856, 0.166, 0.1 ],
        "metallic" : [ 0 ],
        "roughness" : [ 0 ],
        "sheen" : [ 0 ],
        "sheentint" : [ 0 ],
        "clearcoat" : [ 1 ],
        "clearcoatgloss" : [ 0.7 ],
        "speculartint" : [ 0 ],
        "anisotropic" : [ 0 ],
        "eta" : [ 1.5 ],
        "spectrans" : [ 0.8 ],
        "scatterdistance" : [ 0, 0, 0 ],
    },
    "transmission_rough" : {
        "color" : [ 0.856, 0.166, 0.1 ],
        "metallic" : [ 0 ],
        "roughness" : [ 0.7 ],
        "sheen" : [ 0 ],
        "sheentint" : [ 0 ],
        "clearcoat" : [ 1 ],
        "clearcoatgloss" : [ 0.7 ],
        "speculartint" : [ 0 ],
        "anisotropic" : [ 0 ],
        "eta" : [ 1.5 ],
        "spectrans" : [ 0.8 ],
        "scatterdistance" : [ 0, 0, 0 ],
    },
}

indent = "    " * 3

def to_pbrt_string(test_case):
    string = ""
    for key, value in test_case.items():
        T = "float"
        if key in ["color", "scatterdistance"]:
            T = "rgb"
        string += indent + "\"" + T + " " + key + "\" [ " 
        for v in value:
            string += str(v) + " "
        string += "]\n"
    return string

def to_nori_string(test_case):
    string = ""
    for key, value in test_case.items():
        T = "float"
        if key in ["color", "scatterdistance"]:
            T = "color"
        string += indent + "<" + T + " name=\"" + key + "\" value=\"" 
        for i, v in enumerate(value):
            string += str(v)
            if i < len(value) - 1:
                string += ", "
        string += "\"/>\n"
    return string

def generate_scene(test_case_name, test_case, spp):
    pattern = '###material_properties###'
    spp = str(spp)
    spp_pattern = '###spp###'

    nori_name = "nori_autogen/scene_autogen_" + test_case_name
    pbrt_name = "pbrt_autogen/scene_autogen_" + test_case_name
    
    nori_filename = nori_name + '.xml'
    pbrt_filename = pbrt_name + '.pbrt'

    nori_file = nori_template.replace(pattern, to_nori_string(test_case)).replace(spp_pattern, spp)
    pbrt_file = pbrt_template.replace(pattern, to_pbrt_string(test_case)).replace('###output_filename###', pbrt_name + '.exr').replace(spp_pattern, spp)

    with open(nori_filename, "w") as text_file:
        print(nori_file, file=text_file)
    with open(pbrt_filename, "w") as text_file:
        print(pbrt_file, file=text_file)
    pbrt_subprocess = subprocess.Popen(['/home/dfp/work/pbrt-v3/build/pbrt', '/home/dfp/work/blender_mat_test/' + pbrt_filename])
    nori_subprocess = subprocess.Popen(['/home/dfp/work/nori/build/nori', '/home/dfp/work/blender_mat_test/' + nori_filename])
    exit_codes = [subprocess.wait() for subprocess in [pbrt_subprocess, nori_subprocess]]


def generate_all_scenes():
    for test_case_name, test_case in test_cases.items():
        generate_scene(test_case_name, test_case)

# generate_all_scenes()
test_case_name = 'transmission_rough'
test_case = test_cases[test_case_name]
generate_scene(test_case_name, test_case, 512)
