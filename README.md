# Themes directory for third party themes for EdgeTX

For EdgeTX v2.5 compatible themes, please [goto the 2.5 branch](/tree/2.5).

To download all themes, hit the green `Code` button above and choose `Download ZIP`. Alternatively you can git clone the whole repo with a git tool of your choice.

- Contents (ToC):
  * [List of themes available](#list-of-themes-available)
  * [Description of an EdgeTX theme](#description-of-an-edgetx-theme)
  * [Steps to contribute](#steps-to-contribute)

## List of themes available

### RCVR_Halloween
<img src="THEMES/RCVR_Halloween/screenshot1.png" width="240px"> <img src="THEMES/RCVR_Halloween/screenshot2.png" width="240px"> <img src="THEMES/RCVR_Halloween/screenshot3.png" width="240px">

### RCVR_High_Contrast
<img src="THEMES/RCVR_High_Contrast/screenshot1.png" width="240px"> <img src="THEMES/RCVR_High_Contrast/screenshot2.png" width="240px"> <img src="THEMES/RCVR_High_Contrast/screenshot3.png" width="240px">

### RCVR_USA
<img src="THEMES/RCVR_USA/screenshot1.png" width="240px"> <img src="THEMES/RCVR_USA/screenshot2.png" width="240px"> <img src="THEMES/RCVR_USA/screenshot3.png" width="240px">

### InGage_coffee
<img src="THEMES/ingage_coffee/screenshot1.png" width="240px"> <img src="THEMES/ingage_coffee/screenshot2.png" width="240px"> <img src="THEMES/ingage_coffee/screenshot3.png" width="240px">

### InGage_espresso
<img src="THEMES/ingage_espresso/screenshot1.png" width="240px"> <img src="THEMES/ingage_espresso/screenshot2.png" width="240px"> <img src="THEMES/ingage_espresso/screenshot3.png" width="240px">

### InGage_purps
<img src="THEMES/ingage_purps/screenshot1.png" width="240px"> <img src="THEMES/ingage_purps/screenshot2.png" width="240px"> <img src="THEMES/ingage_purps/screenshot3.png" width="240px">

### InGage_carbon
<img src="THEMES/ingage_carbon/screenshot1.png" width="240px"> <img src="THEMES/ingage_carbon/screenshot2.png" width="240px"> <img src="THEMES/ingage_carbon/screenshot3.png" width="240px">

### InGage_poke
<img src="THEMES/ingage_poke/screenshot1.png" width="240px"> <img src="THEMES/ingage_poke/screenshot2.png" width="240px"> <img src="THEMES/ingage_poke/screenshot3.png" width="240px">

### InGage_pastel
<img src="THEMES/ingage_pastel/screenshot1.png" width="240px"> <img src="THEMES/ingage_pastel/screenshot2.png" width="240px"> <img src="THEMES/ingage_pastel/screenshot3.png" width="240px">

### Stroopwafel
<img src="THEMES/Stroopwafel/screenshot1.png" width="240px"> <img src="THEMES/Stroopwafel/screenshot2.png" width="240px"> <img src="THEMES/Stroopwafel/screenshot3.png" width="240px">

### SimpleRed
<img src="THEMES/SimpleRed/screenshot1.png" width="240px"> <img src="THEMES/SimpleRed/screenshot2.png" width="240px"> <img src="THEMES/SimpleRed/screenshot3.png" width="240px">

### RL_Extravagant
<img src="THEMES/RL_Extravagant/screenshot1.png" width="240px"> <img src="THEMES/RL_Extravagant/screenshot2.png" width="240px"> <img src="THEMES/RL_Extravagant/screenshot3.png" width="240px">

### RL_BurgundyRed
<img src="THEMES/RL_BurgundyRed/screenshot1.png" width="240px"> <img src="THEMES/RL_BurgundyRed/screenshot2.png" width="240px"> <img src="THEMES/RL_BurgundyRed/screenshot3.png" width="240px">

### D.Va Pink
<img src="THEMES/DVA_PINK/screenshot1.png" width="240px"> <img src="THEMES/DVA_PINK/screenshot2.png" width="240px"> <img src="THEMES/DVA_PINK/screenshot3.png" width="240px">

## Description of an EdgeTX theme

A theme for EdgeTX consists minimally of 5 files, all sharing the initial part of the filename (**themename** in this example):
  - **themename/theme**.yml (your theme configuration file with name, summary, and color settings)
  - **themename/logo**.png (a logo/banner for your theme)</br>
    ![Example Logo](example/logo.png)
  - **themename/screenshot1.png** (first screenshot, of the main screen with some common widgets selected)</br>
    <img width="240px" src="example/screenshot1.png">
  - **themename/screenshot2.png** (second screenshot, of model selection screen with at least two models present)</br>
    <img width="240px" src="example/screenshot2.png">
  - **themename/screenshot3.png** (third screenshot, of the channel monitor)</br>
    <img width="240px" src="example/screenshot3.png">

Optional:
  - **themename/background_480x272.png** (a background image for your theme in 480 x 272 pixel resolution, e.g. for TX16S, T16, X10, X12S)
  - **themename/background_320x480.png** (a background image for your theme in 320 x 480 pixel resolution, e.g. for NV14)
  - **themename/readme.txt** (any notes or information you wish to share with your theme)

Images should all be in PNG format, and 480x272 pixels in size, except the optional 320x480 background image.

Please refer to the `example` folder for an example of the expected layout.

Please refer to [theme documentation](structure.md) for more information on the theme file format.

## Steps to contribute

Please note that themes are currently still in development phase in EdgeTX and the specification can change. Thus please be prepared that at some point in (near) future you might be asked to update your submission, as we change the specification, e.g. about the image size or YAML style required.

In order to take screenshots using the EdgeTX simulator, first start EdgeTX Companion, pick from menu `Settings` the menu item with similar name `Settings...`
Navigate to `Simulator Settings` tab and provide a folder where you would like the simulator to save the images (here in example `Z:\Multimedia`):

<img src="doc/SimuScreensShotFolder.png">

When using EdgeTX Simulator, click on the Screenshot icon to take a screenshot:

<img src="doc/HowToSimuScreenshot.png" width="250px">

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
