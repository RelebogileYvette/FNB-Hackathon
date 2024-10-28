const categories = Array.from(jCategory)

document.getElementById("searchBar").addEventListener("keyup", (e) => {
    const searchData = e.target.value.toLowerCase();
    const filterData = categories.filter((item) =>
        item.project.toLocaleLowerCase().includes(searchData)
    );
    displayItems(filterData);
});

const displayItems = (items) => {
    const rootElement = document.getElementById('root')
    rootElement.innerHTML = "";

    items.forEach((item) => {
        const {index, image, project, rate, availability} = item;
        const jList = document.createElement("div")
        jList.className = "jList"
        jList.innerHTML = `
        <img src="${image}" alt="">
        <h3>${project}</h3>
        <p>R${rate}</p>
        <span id="key">${availability}</span>
        `
        rootElement.appendChild(jList);

        jList.addEventListener("click", () => {
            window.location.href = `job-details.html?id=${index}`
        });
    });
};

displayItems(categories);