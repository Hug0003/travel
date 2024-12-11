const section2 = document.querySelector("#section--2");
const section1 = document.querySelector("#section--1");
const btnWhite = document.querySelector(".btn--white");
const btnText = document.querySelector(".btn-text");
const btnBack = document.querySelectorAll(".card__side--back-btn");
const btnBox = document.querySelector(".box-btn");
const btnBook = document.querySelector(".btn--book");

const popup = document.querySelector(".popup");
const popupClose = document.querySelector(".popup__close");
const popupContent = document.querySelector(".popup__content");

btnWhite.addEventListener("click", function (e) {
  e.preventDefault();
  const link = e.target.getAttribute("href");
  document.querySelector(link).scrollIntoView({ behavior: "smooth" });
});

btnText.addEventListener("click", function (e) {
  e.preventDefault();
  const link = e.target.getAttribute("href");
  document.querySelector(link).scrollIntoView({ behavior: "smooth" });
});

btnBox.addEventListener("click", function (e) {
  e.preventDefault();
  const link = e.target.getAttribute("href");
  document.querySelector(link).scrollIntoView({ behavior: "smooth" });
});

btnBook.addEventListener("click", function (e) {
  e.preventDefault();
  const link = e.target.getAttribute("href");
  document.querySelector(link).scrollIntoView({ behavior: "smooth" });
});

btnBook.addEventListener("click", function (e) {
  e.preventDefault();
  popup.classList.remove("visible");
  setTimeout(() => {
    popup.classList.add("hidden");
  }, 1000);
});

popupClose.addEventListener("click", function (e) {
  e.preventDefault();
  popup.classList.remove("visible");
  popupContent.classList.remove("visible");

  setTimeout(() => {
    popup.classList.add("hidden");
  }, 1000);
});

btnBack.forEach((btn) =>
  btn.addEventListener("click", function (e) {
    e.preventDefault();
    popup.classList.remove("hidden");
    setTimeout(() => {
      popup.classList.add("visible");
      popupContent.classList.add("visible");
    }, 10);
  })
);
