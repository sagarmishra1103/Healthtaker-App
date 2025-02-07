const body = document.querySelector('body'),
    sidebar = body.querySelector(".sidebar"),
    toggleBtn = body.querySelector(".toggle"),
    searchBtn = body.querySelector(".search-box"),
    modeSwitch = body.querySelector(".toggle-switch"),
    modeText = body.querySelector(".mode-text");


    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("close");
    });
    
    searchBtn.addEventListener("click", () => {
        sidebar.classList.remove("close");
    });
    

    modeSwitch.addEventListener("click", () => {
        body.classList.toggle("dark");

        if (body.classList.contains("dark")) {
            modeText.textContent = "Light Mode"
        } else {
            modeText.textContent = "Dark Mode"
        }
    });


    