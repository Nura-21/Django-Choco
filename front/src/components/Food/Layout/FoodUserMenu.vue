<template>
  <v-menu activator="parent" v-model="$store.foodData.userMenu">
    <v-list>
      <v-list-item
        v-for="item of $store.constants.menuOptions"
        :key="item.id"
        :style="{ 'border-top': item.id === 0 ? '1px solid #eeeeee' : null }"
        style="cursor: pointer"
      >
        <v-list-item-title
          @click="
            item.id !== 0 ? $router.push({ name: item.route }) : $store.logout()
          "
        >
          <i
            v-if="'icon' in item"
            :class="item.icon"
            style="padding-right: 4px"
          ></i>
          {{ item.title }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
export default {
  name: "FoodUserMenu",
  setup() {},
};
</script>
