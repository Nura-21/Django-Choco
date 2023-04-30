<template>
  <v-sheet class="mx-auto" max-width="80vw">
    <v-slide-group
      style="margin-top: 40px"
      prev-icon="fas fa-chevron-left"
      next-icon="fas fa-chevron-right"
      show-arrows
    >
      <v-slide-group-item
        v-for="(category, index) of $store.foodData.categories"
        :key="index"
      >
        <v-card height="140" width="140" style="margin-right: 20px">
          <aside
            @click="
              $store.getFoodRestaurantByCategory(category.id);
              $router.push({
                name: 'foodCategory',
                params: { categoryId: category.id },
              });
            "
            style="
              display: flex;
              flex-direction: column;
              align-items: center;
              cursor: pointer;
            "
          >
            <img
              draggable="false"
              :src="category.img"
              style="width: 80%; height: 80%; user-select: none"
            />
            <span style="font-size: 14px">{{ category.title }}</span>
          </aside>
        </v-card>
      </v-slide-group-item>
    </v-slide-group>
  </v-sheet>
</template>

<script>
export default {
  name: "FoodSlider",
};
</script>
