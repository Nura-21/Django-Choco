import { createRouter, createWebHistory } from "vue-router";
import { routes } from "./routes";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("accessToken");
  if ("requiresAuth" in to.meta && to.meta.requiresAuth && !token) {
    next({
      name: "home",
    });
  } else {
    next();
  }
});

router.afterEach(() => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

export default router;
