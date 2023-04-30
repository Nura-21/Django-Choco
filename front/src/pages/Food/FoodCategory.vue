<template>
  <section class="page category flex flex-col">
    <food-search-block></food-search-block>
    <food-slider></food-slider>
    <food-rest-list></food-rest-list>
  </section>
</template>

<script>
import { useStore } from "@/store";
import { useRoute } from "vue-router";
export default {
  name: "FoodCategory",
  setup() {
    const store = useStore();
    const route = useRoute();

    const initPage = async () => {
      store.isLoading = true;
      await store.getFoodRestaurantByCategory(route.params.categoryId);
      store.isLoading = false;
    };

    initPage();
  },
};
</script>
