const HomePage = () => import("@/pages/HomePage.vue");
// FOOD
const ChocofoodPage = () => import("@/pages/Food/Index.vue");
const FoodCategory = () => import("@/pages/Food/FoodCategory.vue");
const FoodRestaurant = () => import("@/pages/Food/FoodRestaurant.vue");
const UserProfile = () => import("@/pages/Food/UserProfile.vue");

// LIFE
const ChocolifePage = () => import("@/pages/Life/Index.vue");
const LifeEvent = () => import("@/pages/Life/EventPage.vue");
const LifePayment = () => import("@/pages/Life/Payment.vue");

export const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
  },
  {
    path: "/chocofood",
    name: "chocofood",
    component: ChocofoodPage,
  },
  {
    path: "/chocofood/category/:categoryId",
    name: "foodCategory",
    component: FoodCategory,
  },
  {
    path: "/chocofood/restaurant/:id",
    name: "restaurant",
    component: FoodRestaurant,
  },
  {
    path: "/chocofood/account/orders",
    name: "foodOrders",
    component: UserProfile,
  },
  {
    path: "/chocofood/account/bonuses",
    name: "foodBonuses",
    component: UserProfile,
  },
  {
    path: "/chocofood/account/addresses",
    name: "foodAddresses",
    component: UserProfile,
  },
  {
    path: "/chocofood/account/cards",
    name: "foodCards",
    component: UserProfile,
  },
  {
    path: "/chocolife",
    name: "chocolife",
    component: ChocolifePage,
  },
  {
    path: "/chocolife/event/:id/?:event",
    name: "chocolifeEvent",
    component: LifeEvent,
    props: true
  },
  {
    path: "/chocolife/payment",
    name: "chocolifePayment",
    component: LifePayment
  }
].map((route) => {
  if (
    route.name !== "home" &&
    route.name !== "chocolife" &&
    route.name !== "chocofood"
  ) {
    if ("children" in route) {
      route.children.map((childRoute) => {
        if ("meta" in childRoute === false) {
          childRoute.meta = {};
        }
        childRoute.meta.requiresAuth = true;
        return childRoute;
      });
    }
    if ("meta" in route === false) {
      route.meta = {};
    }
    route.meta.requiresAuth = true;
  }
  return route;
});
