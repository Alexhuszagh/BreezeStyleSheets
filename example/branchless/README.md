branchless
==========

This contains an example widget for a `QTreeView` where the branch indicators are hidden. In order to add these branchless indicators to your project, copy this directory into the [extension](/extension) folder, and then configure with (adding any additional resources or styles as you see fit):

```bash
python configure.py --extensions=branchless --resource custom.qrc
```

To remove the branch indicators, you must also set the object name for each `QTreeView` or `QTreeWidget` to `"branchless"`, for example, in Python, `tree.setObjectName("branchless")`.

## Example

<p align="center"><b>Dark</b></p>
<figure>
    <img
        alt="Breeze Dark theme using branchless indicators for Windows"
        src="/assets/breeze_dark_branchless.png"
        title="BreezeDarkBranchless"
    />
</figure>


<p align="center"><b>Light</b></p>
<figure>
    <img
        alt="Breeze Light theme using branchless indicators for Windows"
        src="/assets/breeze_light_branchless.png"
        title="BreezeLightBranchless"
    />
</figure>
