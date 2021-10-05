# Themes directory for third party themes for EdgeTX

*Initial Draft Specification - subject to change!*

A theme for EdgeTX consists of 5 files, all sharing the initial part of the filename:
<ol>
  <li>themefile.yml (where <code>themefile</code> is the name of your theme, and is the same for all files)</li>
  <li>
    themefile.png (a logo/banner for your theme)
    <br><img src="https://raw.githubusercontent.com/EdgeTX/themes/main/example/ETX.png">
  </li>
  <li>
    themefile1.png (first screenshot, of the main screen with some common widgets selected)
    <br><img src="https://github.com/EdgeTX/themes/blob/main/example/ETX1.png">
  </li>
  <li>
    themefile2.png (second screenshot, of model selection screen with at least two models present)  
    <br><img src="https://github.com/EdgeTX/themes/blob/main/example/ETX2.png">
  </li>
  <li>
    themefile3.png (third screenshot, of the channel monitor)  
    <br><img src="https://github.com/EdgeTX/themes/blob/main/example/ETX3.png">
  </li>
</ol>

Images should all be in PNG format, and 225 x 128 pixels in size.

Please refer to the `example` folder for an example of the expected layout.

Please refer to TODO documentation for more information on the theme file format.

## If you are new to GitHub here are the steps to follow in order to contribute

<ol>
  <li>If you do not yet have a GitHub account, create it (it is free)</li>
  <li>Fork this repo by clicking <code>Fork</code> in upper right</li>
  <li>Make a branch (by clicking down arrow at "main" and typing an arbitrary name without spaces, e.g. "mytesttheme" and clicking "Create branch")</li>
  <li>Commit your changes to your newly created branch.
    <br>You can work via GitHub Web interface or optionally you can do this also locally. Instructions for local command line would be:
    <br><code>git clone -b mytesttheme https://github.com/<your user name in GitHub>/themes.git ~/edgetx/themes</code>
    <br>Then add the files with <code>git add</code>, followed by a commit with <code>git commit -m "commitmessagehere"</code> and then push with <code>git push</code>
  <br>If you are a Windows user and looking for a graphical tool for Git, have a look at e.g. <a href="https://tortoisegit.org/">TortoiseGit</a></li>
  <li>Make a pull request by clicking the big green button in GitHub in your fork's branch.</li>
</ol>
