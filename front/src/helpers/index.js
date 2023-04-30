import jwt_decode from "jwt-decode";
import Swal from "sweetalert2";

export const jwtDecode = (token) => {
  return jwt_decode(token);
};

export const getImage = (name) => {
  return new URL(`../assets/${name}`, import.meta.url).href;
};

const Toast = Swal.mixin({
  toast: true,
  position: "bottom",
  showConfirmButton: false,
  timerProgressBar: true,
});

export const showToaster = (icon, title, timer = null) => {
  const config = { icon, title };
  if (timer) {
    config.timer = timer;
  }
  Toast.fire(config);
};
