import axios from "axios";
import interceptors from "./interceptor";

const instance = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
});
interceptors(instance);

export default instance;
