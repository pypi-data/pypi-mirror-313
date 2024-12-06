# **Flow Input Library (FlowInput)**

The library is distributed under the MIT license and can be downloaded and used by anyone.

----------


## How to install
To install, you can download use pip: `pip install FlowInput`

Or download library from the repository from [GitHub](https://github.com/FunsyCode/FlowInput.git)

----------

## Using

----------

### Input
The arguments of main functions are:

#### input():
>prompt: str, default: str, color: Color or BgColor

- **prompt:**     `A String, representing a default message before the input.`
- **default:**    `A String, representing a default message in the input`
- **color:**      `A Color or BgColor Varible, representing Red, Green and Blue colors in the input`

----------
### Colors

The main classes are:

#### Color
**Color:**       `A Class width many Str Variables,  width ANSI codes of colors`

#### BgColor
**BgColor:**     `A Class width many Str Variables, width ANSI codes of background colors`

----------

The arguments of main function are:

#### coloring():
>key: dict, string: str

- **key:**      `A Dict Variable, in which the key is the word that needs to be colored, and the value is the color. Key of dict, have built-in words like this: __start__, __end__, __mid__, __all__. You can see their in examples`
- **string**    `A Str Variable, which is the text to be colored`

----------

## Some examples

**Input**
    
    import FlowInput

    FlowInput.input('What's your name? ', 'My name is Funsy!')

----------
    
**Color**
  
    from FlowInput import colors
    
    print(colors.coloring({'from': colors.Color.BLUE}, 'Hello from FlowInput!'))
    
    print(colors.coloring({'__start__': colors.BgColor.RED}, 'Hello from FlowInput!'))


----------

**Input & Color**
     
    import FlowInput
    
    FlowInput.input('What’s your name? ', 'Funsy', FlowInput.colors.Color.BLUE)
