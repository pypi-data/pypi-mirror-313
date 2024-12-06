
# Table of Contents

1.  [Table of contents](#org08e6727)
2.  [Similar projects](#org0f77488)
3.  [Installation](#org92f7565)
    1.  [Dependencies](#orgae3533d)
    2.  [Installing py5canvas with pip](#org3abe10b)
    3.  [Install locally with pip](#org514cca0)
    4.  [Optional (but suggested) extensions](#org9fe9d03)
4.  [Usage](#orge9ed9c6)
    1.  [Canvas API](#orgd584110)
    2.  [Interactive sketches: py5sketch](#orgec11178)
        1.  [A basic example](#orgf37af21)
        2.  [Main differences with JS/Java](#org4d4af00)
        3.  [Video input and output](#orga38dd6a)
        4.  [Saving SVG output](#org4ca65b5)
        5.  [GUI support and parameters](#org2303733)
        6.  [OSC support](#orgc9b903c)

Py5canvas is a simple library that allows to draw 2d graphics in Python with an interface that is designed for users that are familiar to Processing and P5js.
The library is designed to work inside Python notebooks, as a replacement to Matplotlib and within an appositely built sandbox, for creative coding of simple interactive applications.

The library consists of two main components: The `canvas` API for generating 2d graphics and a command line program `py5sketch` that allows to run the same API interactively. The `canvas` API exposes functionalities similar to Processing and P5js, thus facilitating the composition and generation of 2d graphics. It uses [pyCairo](https://pycairo.readthedocs.io/en/latest/) as a graphics backend, [Matplotlib](https://matplotlib.org) to visualize graphics witin Python notebooks and [NumPy](https://numpy.org) for number-crunching. The `py5sketch` program allows to run and view a Python script (the &ldquo;sketch&rdquo;) that uses the `canvas` API in an interactive window. The program will automatically reload the script whenever it is saved. It uses [Pyglet](https://pyglet.readthedocs.io/en/latest/) as a backend.

The main idea behind this system is to facilitate the development of creative and interactive machine learning applications.


<a id="org08e6727"></a>

# Table of contents


<a id="org0f77488"></a>

# Similar projects

This is one of many ways to develop &ldquo;Processing-like&rdquo; code in Python. There are a number of existing projects with a similar goal:

-   [p5py](https://p5.readthedocs.io/en/latest/) is perhaps the most similar and more mature than this project. It allows to write sketches with a syntax similar to processing in pure Python, and uses on [NumPy](https://numpy.org) and [VisPy](https://vispy.org) as backends.
-   Processing has a [Python mode](https://py.processing.org), but this deviates from the standard way of installing Python dependencies (e.g. Pip or Conda) and makes it more challenging to take full advantage of the big echosystem of Python packages/libraries.
-   [DrawBot](https://www.drawbot.com) uses a different syntax but has a similar goal of easily &ldquo;sketching&rdquo; 2d designs in Python. It currently only runs on MacOS.

The main drive to develop this new system has been to provide a drawing interface in Python notebooks that is similar to Processing and to allow &ldquo;live coding&rdquo; (or more precicesely live-reloading) of interactive sketches for quicker prototyping of ideas. While the syntax of the sketches is similar to P5js or Processing, the aim of this system is to provide a platform similar to DrawBot for interactive editing of scripts and with a focus on 2d vector graphics.


<a id="org92f7565"></a>

# Installation


<a id="orgae3533d"></a>

## Dependencies

The main requirements for Py5Canvas are [NumPy](https://numpy.org), [Matplotlib](https://matplotlib.org), [pyCairo](https://pycairo.readthedocs.io/en/latest/) and [Pyglet](https://pyglet.readthedocs.io/en/latest/). Pyglet is only necessary if you want to use interactivity but it will be automatically installed with the procedure described in the next section. To fully use the Canvas API with video input, you will also need [OpenCV](https://opencv.org), The instructions below include it, but it is not essential.
The dependency installation procedure depends on the [conda package mananger](https://docs.conda.io/en/latest/). With many different options, one ideal way to install conda is to use the reduced [miniforge](https://github.com/conda-forge/miniforge) installer (saves disk space). To speed up installation, it is recommended to install [mamba](https://mamba.readthedocs.io/en/latest/) alongside conda (since &ldquo;vanilla&rdquo; conda is written in Python and can be extremely slow). Once a version of conda is installed, install mamba with:

    conda install conda-forge::mamba

Afterwards, you can pretty much replace any use of `conda` with `mamba` and things will go significantly faster.

You might want to create a conda Python environment before going forward, which means you will be able to install the dependencies without interfering with your base Python installation. To do so you can do:

    conda create -n py5 python=3.10

and then

    conda activate py5

Finally, install the required dependencies with (use mamba if installed):

    conda install -c conda-forge numpy matplotlib pycairo opencv


<a id="org3abe10b"></a>

## Installing py5canvas with pip

py5canvas is still not on PyPi, so for the moment you can use one of the following to install:

    pip install git+https://github.com/colormotor/py5canvas.git

To update the module to its latest version use

    pip install --upgrade  --force-reinstall --no-deps git+https://github.com/colormotor/py5canvas.git

Then install the latest version of Pyglet with

    pip install pyglet


<a id="org514cca0"></a>

## Install locally with pip

With this procedure, you will be able to pull the latest changes to the module with git. Firt, clone the repository in a given directory, e.g. with

    git clone https://github.com/colormotor/py5canvas.git

or by using your Git frontend of choice.
Then navigate to the `py5canvas` directory and install locally with

    pip install -e .

Now any modification to the code in the directory will be always available when you import hte module.


<a id="org9fe9d03"></a>

## Optional (but suggested) extensions

1.  Open Sound Control (OSC)

    The sketch interface also provides optional OSC functionality through the  [python-osc](https://pypi.org/project/python-osc/) module. This enables communication with other software that supports the protocol. It can be installed with:
    
        pip install python-osc
    
    See the relevant section below for usage details.


<a id="orge9ed9c6"></a>

# Usage


<a id="orgd584110"></a>

## Canvas API

Once installed you can use the canvas API in a notebook (or Python program) by simply importing it. This is a simple example that will save an image and show it with Matplotlib:

    from py5canvas import canvas
    
    # Create our canvas object
    c = canvas.Canvas(512, 512)
    
    # Clear background to black
    c.background(0)
    # Set stroke only and draw circle
    c.stroke(128)
    c.no_fill()
    c.stroke_weight(5)
    c.circle(c.width/2, c.height/2, 100)
    # Draw red text
    c.fill(255, 0, 0)
    c.text_size(30)
    c.text([c.width/2, 40], "Hello world", center=True)
    # Save image
    # c.save_image('./images/canvas.png')
    c.show()

![img](./images/canvas.png)

In general, the syntax is very similar to P5js but it uses `snake_case` as a syntax convention, and it requires explicitly referencing a `Canvas` object rather than exposing this functionality globally. For more detailed instructions refer to [this notebook](https://github.com/colormotor/py5canvas/blob/main/examples/canvas_tutorial.ipynb).

> The Canvas object is intended to be a simple interface on top of [pyCairo](https://pycairo.readthedocs.io/en/latest/), but it does not expose all the functionalities of the API. If necessary, these can be accessed with the `ctx` class variable.


<a id="orgec11178"></a>

## Interactive sketches: py5sketch

While the Canvas API alone does not supprt interactivity, the `py5sketch` program allows to create simple &ldquo;sketches&rdquo; that can be run interactively in a window.


<a id="orgf37af21"></a>

### A basic example

Let&rsquo;s look at a simple example (`basic_animation.py`) that generates a rotating circle that leaves a trail behind

    def setup():
        create_canvas(512, 512)
    
    def draw():
        background(0, 0, 0, 8) # Clear with alpha will create the "trail effect"
        push()
        # Center of screen
        translate(c.width/2, c.height/2)
        # Draw rotating circle
        fill(255, 0, 0)
        stroke(255)
        rotate(sketch.frame_count*0.05)
        circle(100, 0, 20)
        pop()

To run this script navigate to the directory where it is located and from the command line run

    py5sketch basic_animation.py

This will open a window with the sketch.

Similarly to P5js and Processing, the sketch revolves around two functions: `setup` and a `draw`. The first is called once and can be used to setup the sketch. The second is called every frame and can be used to update our animation.

1.  Running a script standalone

    Running a script with the method above allows to edit a script and reload it every time it is saved. To run a script &ldquo;standalone&rdquo; and disable live reloading, add the following to the end of the script:
    
        if __name__== '__main__':
            import py5canvas
            py5canvas.run()
    
    And the run the script with
    
        python basci_animation.py
    
    replacing \`basic<sub>animation.py</sub>\` with your script name.
    
    This will result in a behavior similar to [p5py](https://p5.readthedocs.io/en/latest/) where you need to re-run a script every time edits are made.


<a id="org4d4af00"></a>

### Main differences with JS/Java

In general the structure and syntax of a sketch is very similar to P5js or Processing. The main difference is the &ldquo;snake<sub>case</sub>&rdquo; convention, so function and variable names have words separated by underscores and not capitals. As an example the function `createCanvas` will be `create_canvas` instead. Similarly, you can equivalently use `size` instead of the `createCanvas` function.

However, there are a number of differences to take into account.

1.  Globals

    Differently from Javascript or Java, Python does not allow modifications to globals from within a function by default. For example this code snippet
    
        foo = 10
        def draw():
            print(foo)
            foo += 1
    
    will print the value of `foo` but incrementing the variable will not work. To make this work we need to explicitly declare
    `foo` as a global. In the following example we declare two variables as globals allowing the function to modify both.
    
        foo = 10
        bar = 20
        def draw():
            global foo, bar
            foo += 1
            bar -= 1
    
    1.  Avoiding globals with a container
    
        One way to avoid haing to declare globals every time is to put the parameters that can be modified within a function inside a container. As an example, we could use an anonymous function or an [EasyDict](https://pypi.org/project/easydict/) dictionary. The anonymous function trick would be as follows:
        
            params = lambda: None
            params.foo = 10
            params.bar = 20
            
            def draw():
                params.foo += 1
                params.bar -= 1
        
        An alternative, that is also useful to automatically create a GUI and save/load parameters is using [EasyDict](https://pypi.org/project/easydict/), which allows accessing elements of a dictionary without using quotes:
        
            from easydict import EasyDict as edict
            params = edict({
                'foo': 10,
                'bar': 20 })
            
            def draw():
                params.foo += 1
                params.bar -= 1
        
        Refer to the section on GUI and parameters to see how this can also be used to handle sketch parameters.

2.  Converting a p5js sketch

    One quick and dirty way to convert a p5js sketch to a Python py5sketch is to use ChatGPT. This prompt seems to work relatively well
    
    > Convert this code to Python using camel case instead of snake case, but keeping exactly the same function and variable names, don&rsquo;t capitalize variables:
    
    Followed by the p5js code.
    The [L-system](https://github.com/colormotor/py5canvas/blob/main/examples/l_system.py) and [spirograph](https://github.com/colormotor/py5canvas/blob/main/examples/spirograph.py) examples have been converted this way from the p5js example library, with little to no modifications.

3.  The `sketch` and `canvas` objects

    Behind the hood a sketch uses two main components: A `sketch` object that
    handles the script running and updates and a `sketch.canvas` object that handles
    drawing 2d graphics.
    
    By default, the `py5sketch` program exposes the methods of these objects as
    globals, so it is not necessary to reference these objects explicitly. However,
    while easy to remember, function names like `scale`, `rotate` etc, are quite
    common words and it is easy to overwrite them by mistake while writing a script.
    For example this sketch won&rsquo;t work:
    
        scale = 1.0
        
        def setup():
            create_canvas(512, 512)
        
        def draw():
            background(0)
            translate(width/2, height/2)
            scale(0.5)
            circle(0, 0, 100)
    
    Since we have overridden the function `scale` with a variable `scale`. We can
    avoid these situations by referring to the canvas (or sketch explicitly), with a
    variable `c` automatically set to refer to the `sketch.canvas` object (for
    brevity). So the following will work:
    
        scale = 1.0
        
        def setup():
            sketch.create_canvas(512, 512)
        
        def draw():
            c.background(0)
            c.translate(c.width/2, c.height/2)
            c.scale(0.5)
            c.circle(0, 0, 100)
    
    We could identically refer to `c` as `sketch.canvas`.


<a id="orga38dd6a"></a>

### Video input and output

With OpenCV installed, the py5sketch systems allows to read the webcam stream, play videos and to save videos of the sketch output.

1.  Playing video

    To show the webcam input or to play a video, you need to use the `canvas.VideoInput` object. It takes one optional parameter that is either the video input device number (`0` is the default) or the name of a file to play. See [the video input example](https://github.com/colormotor/py5canvas/blob/main/examples/video_input.py) for details.

2.  Saving video or image sequences

    To save a specified number of frames as a video or as an image sequence, use the the
    `sketch.grab_movie(filename, num_frames, framerate)` and `sketch.grab_image_sequence(directory_name, num_frames)` functions. As an example, calling `sketch.grab_move("frames.mp4", 200, 30)` will save a 30 FPS mp4 movie of 200 frames. Both functions have an optional argument `reload` that is set to `True`. If `reload` is `True`, the script is reloaded when saving so the video will start from the first frame. This is particularly useful when saving loops. If `reload=False`, the video will start recording from the next frame without reloading.


<a id="org4ca65b5"></a>

### Saving SVG output

All vector drawing operations for a given frame, can be exported to SVG by using the GUI (if [PyImGui](https://pypi.org/project/imgui/#files) is installed), or by using the `sketch.save_svg(filename)` function.
Note that once called, the **next** frame will be saved.


<a id="org2303733"></a>

### GUI support and parameters

The `py5sketch` program can be used in combination with the [Python bindings](https://pypi.org/project/imgui/#files) of [Dear ImGui](https://github.com/ocornut/imgui), an [&ldquo;immediate mode&rdquo; UI](https://pyimgui.readthedocs.io/en/latest/guide/first-steps.html#what-is-immediate-mode-gui) built on top of OpenGL. A basic usage example of IMGUI can be found in the `imgui_test.py` example.

1.  Default UI

    If pyImGui is installed, the `py5sketch` program will feature a basic toolbar. The toolbar allows to:
    
    -   Load a sketch
    -   Backup a sketch
    -   Reload the current sketch
    -   Save the output for the current sketch as a SVG file.
    
    &ldquo;Backing up a sketch&rdquo; means that the current sketch, and its parameters (see the following) will be saved with the name specified. This can be useful to save the current iteration of a sketch while continuing to work on the code. E.g. say you are working on a sketch and realize you like the results, but this is not the final result you where trying to achieve. You can &ldquo;backup&rdquo; the sketch and then eventually go back to the code later, while continue working on the current sketch and not risking to destroy the achieved result.

2.  Parameters and automatic GUI

    While one can use the immediate mode paradigm to create a dynamic UI in the `draw` function, it is also possible to automatically create an UI for a given number of parameters.
    The parameters are defined by passing a dictionary to the `sketch.parameters` function, e.g.:
    
        params = {'Width': (100, {'min': 10, 'max': 200}),
                  'Height': (100, {'min': 10, 'max': 200}),
                  'rectangle color': ([255, 0, 0], {'type':'color'})}
        params = sketch.parameters(params)
    
    ![img](./images/params.jpg)
    
    This syntax defines the parameters and then uses the `sketch.parameters` function to tell `py5sketch` that we will be using these. The function returns a new dictionary that can be used more conveniently by the sketch. If [EasyDict](https://pypi.org/project/easydict/) is installed, the parameters can be more conveniently accessed with the dot notation, e.g. `params.width` or `params.rectangle_color`. Note that the parameter names we defined contain spaces and capitals. These will be automatically converted to names that are all lower-case and with spaces replaced by underscores. The names originally specified will instead appear by deault as labels when the GUI is created.
    
    You can create groups/subparameters (also in the GUI) by adding an entry to the dictionary that is a dictionary itself. See the `parameters.py` script for an example.
    
    1.  Saving and loading
    
        The `py5sketch` program will automatically save and load the parameters when reloading a sketch or closing the program. However, note that the parameters will NOT be saved if the script has an error.
    
    2.  Presets
    
        When parameters are defined as above, the UI will automatically show a &ldquo;Presets&rdquo; header. Typing a name in the &ldquo;Name&rdquo; input field will allow to save a presets with the given name.
    
    3.  Showing the GUI
    
        If parameters are defined, an UI for the parameters will be visualized on the right of the canvas. The window will be resized so it can fit the canvas of the specified size together with the UI. You can specify the size of the UI (e.g. for accommodating longer parameter names) by specifying the optional `gui_width` parameter when calling `create_canvas`. E.g.:
        
            def setup():
                create_canvas(512, 512, gui_width=300)
        
        Will add `300` pixels to the window width in order to show a column containing the parameter UI.
    
    4.  Parameter widget types
    
        When automatically creating a GUI, the `py5sketch` program uses the type of the parmameter and options to infer what widget will be visualized:
        
        1.  Boolean
        
            -   Widget: **Checkbox**
            -   Options: None
        
        2.  Integer
        
            -   Widget: Integer input field, Integer slider or Combo (dropdown selection).
            -   Options:
                -   **Value box** (no options specified)
                -   **Slider** (`min` and `max` options are specified)
                -   **Combo** (`selection` is specified with a list of strings)
        
        3.  Float
        
            -   Widget: Float input field or Float slider
            -   Options:
                -   **Value box** (no options specified)
                -   **Slider** (`min` and `max` options are specified)
        
        4.  String
        
            -   Widget: Single-line or multi-line text input field
            -   Options:
                -   Maximum buffer length, `buf_length` key in opts (default to: `1024`)
                -   **Multiline text input** if the `multiline:True` option is defined.
        
        5.  Callable (the name of a function)
        
            -   Widget: **Button**
            -   Options: None
        
        6.  Float Array
        
            -   Widget: Value boxes, sliders or a color picker
            -   Options:
                -   **Color selector** if the `type='color'` option is specified. The length of the array must be 3 or 4.
                -   **Sliders** if the `min` and `max` options are specified
                -   **Value boxes** if no options are specified
        
        7.  Integer Array
        
            -   Widget: Value boxes, sliders or a color picker
            -   Options:
                -   **Sliders** if the `min` and `max` options are specified
                -   **Value boxes** if no options are specified

3.  Auto saving

    Creating parameters as described above will result in the parameters being automatically saved and loaded every time a sketch is reloaded. The parameters will be saved to a JSON file having the same name and directory as the sketch script.


<a id="orgc9b903c"></a>

### OSC support

If [python-osc](https://pypi.org/project/python-osc/) is installed, py5sketch automatically initializes an OSC server and client.
By default, the client will run on localhost address (127.0.0.1) with port 9998,
and the server will listen on port 9999 for any incoming OSC message.

You can configure these parameters by creating an `osc.json` file that is located in the same directory as the script.
A default setup would look like this

    {
        'server port': 9999,
        'client address': 'localhost',
        'client port': '9998'
    }

These parameters will not change until you restart py5sketch.

If a `received_osc(addr, value)` function is defined in the sketch, this will be automatically called any time an OSC message is received, with `addr` containing the messsage address (as a string) and `value` containing the message contents.

To send an osc message at any time, use the `sketch.send_osc(addr, value)`.

See the <./examples/osc_example.py> script and the <./examples/osc_example.maxpat> Max MSP patch for a usage example.

