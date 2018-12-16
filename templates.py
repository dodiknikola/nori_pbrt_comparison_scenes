pbrt_template = \
"""
Integrator "path" "integer maxdepth" [ 65 ] "float rrthreshold" [ 65 ]
Sampler "random" "integer pixelsamples" [ ###spp### ] 
PixelFilter "triangle" "float xwidth" [ 1.000000 ] "float ywidth" [ 1.000000 ] 
Film "image" "integer xresolution" [ 720 ] "integer yresolution" [ 720 ] "string filename" [ "###output_filename###" ] 
LookAt 50 -20 50 # eye
       0 0 0    # look at point
       0 0 1    # up vector
Camera "perspective" "float fov" [ 30 ] 
WorldBegin
    # Material definitions
	MakeNamedMaterial "White" "string type" [ "matte" ] "rgb Kd" [ 1 1 1 ] "float sigma" [ 0 ]
	MakeNamedMaterial "Material" "string type" [ "disney" ]
###material_properties###

    # Lights
    AttributeBegin
        AreaLightSource "diffuse" "rgb L" [ 15 15 15 ]
        Shape "plymesh" "string filename" [ "models/LightPlaneBig.001.ply" ] 
    AttributeEnd

    # Material object
    AttributeBegin
	    NamedMaterial "Material" 
		Shape "plymesh" "string filename" [ "models/SolidModel.ply" ] 
    AttributeEnd

    # Rest of the scene
    AttributeBegin
	    NamedMaterial "White" 
		Shape "plymesh" "string filename" [ "models/Base.001.ply" ] 
		Shape "plymesh" "string filename" [ "models/EnvironmentLetter.ply" ] 
		Shape "plymesh" "string filename" [ "models/TextBase.001.ply" ] 
    AttributeEnd
    AttributeBegin
        Texture "checks" "spectrum" "checkerboard"
              "float uscale" [100] "float vscale" [100]
              "rgb tex1" [.8 .8 .8] "rgb tex2" [.2 .2 .2]
	    Material "matte" "texture Kd" "checks" 
		Shape "plymesh" "string filename" [ "models/MeasurementRig.001.ply" ] 
    AttributeEnd
    AttributeBegin
        Texture "checks" "spectrum" "checkerboard"
              "float uscale" [10] "float vscale" [10]
              "rgb tex1" [1 1 1] "rgb tex2" [.2 .2 .2]
	    Material "matte" "texture Kd" "checks" 
		Shape "plymesh" "string filename" [ "models/CoreSolidMaterial.ply" ] 
    AttributeEnd
WorldEnd
"""

nori_template = \
"""
<?xml version="1.0" encoding="utf-8"?>

<scene>
    <integrator type="path_mis">
        <integer name="maxdepth" value="65"/>
    </integrator>

	<camera type="perspective">
		<float name="fov" value="30" />
		<transform name="toWorld" >
            <lookat origin="50, 50, 20" target="0, 0, 0" up="0, 1, 0"/>
		</transform>

        <integer name="width" value="720" />
        <integer name="height" value="720" />
        <rfilter type="tent"/>
	</camera>

	<sampler type="independent">
		<integer name="sampleCount" value="###spp###"/>
	</sampler>

    <!-- Lights -->
	<mesh type="obj">
		<string name="filename" value="models/LightPlaneBig.001.obj"/>
		<emitter type="area">
			<color name="radiance" value="15 15 15"/>
		</emitter>
	</mesh>

    <!-- Material object -->
	<mesh type="obj" >
		<string name="filename" value="models/SolidModel.obj" />
        <bsdf type="disney" id="Material">
###material_properties###
        </bsdf>
	</mesh>

    <!-- Rest of the scene -->
	<mesh type="obj" >
		<string name="filename" value="models/Base.001.obj" />
        <bsdf type="diffuse" id="White">
            <color name="albedo" value="1, 1, 1"/>
        </bsdf>
	</mesh>

	<mesh type="obj" >
		<string name="filename" value="models/CoreSolidMaterial.obj" />
        <bsdf type="diffuse" id="White">
            <texture type="checkerboard_color" name="albedo">
                    <point name="delta" value="0, 0"/>
                    <vector name="scale" value="0.1,0.1"/>
                    <color name="value1" value="1, 1, 1"/>
                    <color name="value2" value="0.2,0.2,0.2"/>
            </texture>
        </bsdf>
	</mesh>

	<mesh type="obj" >
		<string name="filename" value="models/EnvironmentLetter.obj" />
        <bsdf type="diffuse" id="White">
            <color name="albedo" value="1, 1, 1"/>
        </bsdf>
	</mesh>

	<mesh type="obj" >
		<string name="filename" value="models/MeasurementRig.001.obj" />
		<bsdf type="diffuse">
            <texture type="checkerboard_color" name="albedo">
                    <point name="delta" value="0, 0"/>
                    <vector name="scale" value="0.01,0.01"/>
                    <color name="value1" value="0.8,0.8,0.8"/>
                    <color name="value2" value="0.2,0.2,0.2"/>
            </texture>
		</bsdf>
	</mesh>

	<mesh type="obj">
		<string name="filename" value="models/TextBase.001.obj"/>
        <bsdf type="diffuse" id="White">
            <color name="albedo" value="1, 1, 1"/>
        </bsdf>
	</mesh>
</scene>
"""
