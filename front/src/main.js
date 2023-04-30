import { createApp, markRaw } from "vue";
import { createPinia } from "pinia";
import { api } from "@/api";
import { getImage } from "./helpers";
import { useStore } from "@/store";

import App from "./App.vue";
import router from "./router";
import components from "@/components";
import vuetify from "./plugins/vuetify";
import Maska from "maska";
import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

import "./styles/styles.scss";

const app = createApp(App);

app.component("Datepicker", Datepicker);
components.forEach((component) => {
  app.component(component.name, component);
});

const pinia = createPinia();
pinia.use(({ store }) => {
  store.router = markRaw(router);
  return { api };
});

app.use(pinia).use(router).use(vuetify).use(Maska);

app.config.globalProperties.$getImage = getImage;
app.config.globalProperties.$store = useStore();

app.mount("#app");
