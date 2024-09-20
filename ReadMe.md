<h2 id="explanation">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Star.svg" width="30px" align="top"/>
    ⠀Unit Tests Submodule
</h2>

<p>This repository is designed to be used as a submodule where I create unit tests for my projects. </p>

<h2 id="usage">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Gear.svg" width="30px" align="top"/>
    ⠀How to Use Submodules
</h2>

- ### Clone Main Repository Including Submodules

    ```bash
    git clone --recurse-submodules <main-repo-url>
    ```

    If you have already cloned the repository without the `--recurse-submodules` option, it can still be initialized by running:

    ```bash
    git submodule update --remote --merge
    ```

    Or:

    ```bash
    git submodule init
    git submodule update
    ```

- ### Check Submodules Version

    ```bash
    git submodule status
    ```

- ### Update Submodules

    If changes are made to this repository, developers will need to pull them by running:

    ```bash
    git submodule update --remote
    ```

- ### Committing Changes to the Submodule Repository

    If a developer modifies the submodule, they need to commit the changes in this repository and then commit the updated submodule reference in the main project:

    - #### Inside the submodule directory:

        ```bash
        git add <new-files>
        git commit -m "Updated submodule"
        ```
    
    - #### Then, in the main project directory:

        ```bash
        git add <submodule-folder>
        git commit -m "Updated Tests submodule"
        ```
    
    If you try to commit from the main project directory without committing the submodule first, you will see a message like this: 

    ```bash
    warning: not adding submodule <submodule-folder>
    ```

    And the changes will not be commited to this repository. Submodules in Git are independent repositories, meaning that when you modify files within a submodule, Git will not automatically track these changes when you're in the main project directory.