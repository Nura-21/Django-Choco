<template>
  <div class="search-block">
    <section class="search-block-container">
      <v-text-field
        v-model="searchQuery"
        label="Название заведения или блюда"
        variant="solo"
        hide-details
        class="shadow"
      ></v-text-field>
      <food-green-button
        text="Найти"
        size="lg"
        @click="$store.searchRest(searchQuery)"
      ></food-green-button>
      <aside class="search-block-queries">
        <span>Популярные запросы</span>
        <div>
          <span
            v-for="(query, index) of $store.foodData.categories"
            :key="query.id"
          >
            <span
              class="cursor-pointer"
              v-if="index < 4"
              @click="
                $store.getFoodRestaurantByCategory(query.id);
                $router.push({
                  name: 'foodCategory',
                  params: { categoryId: query.id },
                });
              "
              >{{ query.title }}</span
            >
          </span>
        </div>
      </aside>
    </section>
  </div>
</template>

<script>
import { ref, watch } from "vue";
import { useStore } from "@/store";

export default {
  name: "FoodSearchBlock",
  setup() {
    const store = useStore();
    const searchQuery = ref("");
    const popularQueries = [
      { name: "Суши" },
      { name: "Грузинская кухня" },
      { name: "Бургер" },
      { name: "Суп с гречей" },
    ];

    watch(
      () => searchQuery.value,
      async () => {
        if (searchQuery.value.length === 0) {
          store.isLoading = true;
          await store.getFoodRestList();
          store.isLoading = false;
        }
      }
    );

    return {
      searchQuery,
      popularQueries,
    };
  },
};
</script>
