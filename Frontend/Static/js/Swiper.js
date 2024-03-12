document.addEventListener('DOMContentLoaded', function () {
  var swiper = new Swiper('.swiper-container', {
    // Your Swiper settings here
    mousewheel: {
      invert: false,
    },
    spaceBetween: 20,
  });
});

window.onload = () => {
  sessionStorage.removeItem('paymentMade')
}