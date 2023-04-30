export default function (axios) {
  axios.interceptors.request.use(
    (request) => {
      if (
        request.url &&
        request.url.at(-1) !== "/" &&
        request.url.includes("?") === false
      ) {
        request.url += "/";
      }
      const token = localStorage.getItem("accessToken");
      if (token) {
        request.headers.Authorization = localStorage.getItem("accessToken");
      }
      return request;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
}
