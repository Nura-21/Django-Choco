<template>
  <v-overlay
    :model-value="$store.isLoading"
    class="align-center justify-center"
  >
    <v-progress-circular
      indeterminate
      size="64"
      color="red"
    ></v-progress-circular>
  </v-overlay>
  <div :class="{ 'bg-gray-200': isLife }">
    <LifeHeader v-if="isLife"></LifeHeader>
    <FoodHeader v-if="isFood"></FoodHeader>
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
    <LifeFooter v-if="isLife"></LifeFooter>
    <FoodFooter v-if="isFood"></FoodFooter>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import { watch, ref } from "vue";
import { useStore } from "@/store";

const store = useStore();
const route = useRoute();

const isLife = ref(false);
const isFood = ref(false);

const handleProducts = (title, link, appClass) => {
  const favicon = document.getElementById("favicon");
  const appTitle = document.getElementById("title");
  const app = document.getElementById("app");
  if (appClass !== null) {
    app.classList.add(appClass);
  } else {
    app.classList = [];
  }
  if (title !== null) {
    appTitle.innerHTML = title;
  } else {
    appTitle.innerHTML = "Проект Choco";
  }

  favicon.href = link;
};

handleProducts(null, "favicon.ico", null);

watch(
  () => route.fullPath,
  (routePath) => {
    if (routePath.includes("chocolife")) {
      isFood.value = false;
      isLife.value = true;
      handleProducts("Chocolife", store.constants.lifeFavicon, "life");
      return;
    }
    if (routePath.includes("chocofood")) {
      isLife.value = false;
      isFood.value = true;
      handleProducts("Chocofood", store.constants.foodFavicon, "food");
      return;
    }
    isLife.value = false;
    isFood.value = false;
    handleProducts(null, "favicon.ico", null);
  }
);

store.initData();
</script>