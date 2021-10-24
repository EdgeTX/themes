# Themes directory for third party themes for EdgeTX

- Contents (ToC):
  * [List of themes available](#list-of-themes-available)
  * [Description of an EdgeTX theme](#description-of-an-edgetx-theme)
  * [Steps to contribute](#steps-to-contribute)

## List of themes available

### RCVR_Halloween
<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/RCVR_Halloween1.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/RCVR_Halloween2.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/RCVR_Halloween3.png" width="240px">

### InGage_coffee
<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_coffee1.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_coffee2.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_coffee3.png" width="240px">

### InGage_espresso
<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_espresso1.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_espresso2.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_espresso3.png" width="240px">

### InGage_purps
<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_purps1.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_purps2.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_purps3.png" width="240px">

### InGage_carbon
<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_carbon1.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_carbon2.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_carbon3.png" width="240px">

### InGage_poke
<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_poke1.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_poke2.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_poke3.png" width="240px">

### InGage_pastel
<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_pastel1.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_pastel2.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/ingage_pastel3.png" width="240px">

### RCVR_High_Contrast
<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/RCVR_High_Contrast1.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/RCVR_High_Contrast2.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/RCVR_High_Contrast3.png" width="240px"> 

### Stroopwafel
<img width="240px" src="https://github.com/Str00pwafel/themes/blob/main/THEMES/stroopwafel1.png"> <img width="240px" src="https://github.com/Str00pwafel/themes/blob/main/THEMES/stroopwafel2.png"> <img width="240px" src="https://github.com/Str00pwafel/themes/blob/main/THEMES/stroopwafel3.png">

### SimpleRed
<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/SimpleRed1.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/SimpleRed2.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/SimpleRed3.png" width="240px">

### Extravagant
<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/Extravagant1.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/Extravagant2.png" width="240px"> <img src="https://raw.githubusercontent.com/EdgeTX/themes/main/THEMES/Extravagant3.png" width="240px">

## Description of an EdgeTX theme

In EdgeTX 2.5, themes only really comprise of the following:
  - **themefile**.yml (your theme configuration file with name, summary, and color settings)
  - **themefile**.png (a logo/banner for your theme)</br>

No other files are used by the transmsmitter firmware, and the **themefile**.png is itself not strictly necessary for the theme to function. 

However, moving forward to EdgeTX 2.6, it is envisaged that themes will also be able to provide a background, and that the end user will have more control over what is displayed  when. Thus, the following draft specification as to how a theme will look, which will be expected as of EdgeTX 2.6, and as it is still in draft form, subject to change as it continues to evolve. 

*Initial Draft Specification - subject to change!*

A theme for EdgeTX consists minimally of 5 files, all sharing the initial part of the filename (**themefile** in this example):
  - **themefile**.yml (your theme configuration file with name, summary, and color settings)
  - **themefile**.png (a logo/banner for your theme)</br>
    ![Example Logo](example/ETX.png)
  - **themefile**1.png (first screenshot, of the main screen with some common widgets selected)</br>
    <img width="240px" src="example/ETX1.png">
  - **themefile**2.png (second screenshot, of model selection screen with at least two models present)</br>
    <img width="240px" src="example/ETX2.png">
  - **themefile**3.png (third screenshot, of the channel monitor)</br>
    <img width="240px" src="example/ETX3.png">

Optional:
  - **themefile**_bg_480x272.png (a background image for your theme in 480 x 272 pixel resolution, e.g. for TX16S, T16, X10, X12S)
  - **themefile**_bg_320x480.png (a background image for your theme in 320 x 480 pixel resolution, e.g. for NV14)
  - **themefile**_readme.txt (any notes or information you wish to share with your theme)

Images should all be in PNG format, and 480x272 pixels in size, except the optional 320x480 background image.

Please refer to the `example` folder for an example of the expected layout.

Please refer to TODO documentation for more information on the theme file format.

## Steps to contribute

Please note that themes are currently still in development phase in EdgeTX and the specification can change. Thus please be prepared that at some point in (near) future you might be asked to update your submission, as we change the specification, e.g. about the image size or YAML style required.

In order to take screenshots using the EdgeTX simulator, first start EdgeTX Companion, pick from menu `Settings` the menu item with similar name `Settings...`
Navigate to `Simulator Settings` tab and provide a folder where you would like the simulator to save the images (here in example `Z:\Multimedia`):

<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/doc/SimuScreensShotFolder.png">

When using EdgeTX Simulator, click on the Screenshot icon to take a screenshot:

<img src="https://raw.githubusercontent.com/EdgeTX/themes/main/doc/HowToSimuScreenshot.png" width="250px">

If you want to contribute at current early stage in spite of the warning above, here are the steps:
<ol>
  <li>If you do not yet have a GitHub account, create it (it is free)</li>
  <li>Fork this repo by clicking <code>Fork</code> in upper right</li>
  <li>Make a branch (by clicking down arrow at "main" and typing an arbitrary name without spaces, e.g. "mytesttheme" and clicking "Create branch")</li>
  <li>Commit your changes to your newly created branch.
    <br>You can work via GitHub Web interface or optionally you can do this also locally. Instructions for local command line would be:
    <br><code>git clone -b mytesttheme https://github.com/your_user_name_in_GitHub/themes.git ~/edgetx/themes</code>
    <br>Then add the files with <code>git add</code>, followed by a commit with <code>git commit -m "commitmessagehere"</code> and then push with <code>git push</code>
  <br>If you are a Windows user and looking for a graphical tool for Git, have a look at e.g. <a href="https://tortoisegit.org/">TortoiseGit</a></li>
  <li>Make a pull request by clicking the big green "Compare & Pull Request" button in GitHub in your fork's branch.</li>
</ol>
