const sortBtns = document.querySelectorAll(".job-id > li")
const sortItems = document.querySelectorAll(".jobs-container .jList")
                
sortBtns.forEach((btn) =>{
    btn.addEventListener('click', () => {
        sortBtns.forEach((btn) => btn.classList.remove
        ("active"))
        btn.classList.add("active")

        

        const targetData = btn.getAttribute('data-target')

        sortItems.forEach((item) => {
            item.classList.add('hidden');
            if (item.getAttribute('data-item') === targetData || targetData == "all") {
                item.classList.remove('hidden');
            }
        });
    });
});


