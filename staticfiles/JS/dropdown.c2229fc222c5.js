const profilephotodiv = document.querySelector(".profile__photo");
const profilephoto = profilephotodiv.querySelector("img");
const dropdownmenu = profilephotodiv.querySelector(".profile-dropdown");

profilephotodiv.addEventListener("click", (_) => {
    console.log('added');
    dropdownmenu.classList.toggle("dropdown-is-visible");
});
