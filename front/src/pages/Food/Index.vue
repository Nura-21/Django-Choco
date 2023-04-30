<template>
  <section v-if="$store.hasLogged" class="page flex flex-col">
    <food-search-block></food-search-block>
    <food-slider></food-slider>
    <food-rest-list></food-rest-list>
  </section>
  <main v-if="$store.hasLogged === false" class="food-main">
    <aside class="food-main-left">
      <h2>
        <span>Chocofood</span> - сервис доставки еды в
        <span>{{ $store.user.city }}</span>
      </h2>
      <h2>Ваш <span>адрес доставки</span></h2>
      <div class="food-main-left-input">
        <MapIcon />
        <input
          class="shadow"
          placeholder="Введите адрес доставки"
          type="text"
        />
      </div>
      <button class="food-btn food-btn-green shadow">НАЙТИ ЗАВЕДЕНИЯ</button>
    </aside>
    <aside class="food-main-right">
      <img
        draggable="false"
        src="https://chocofood.kz/images/start/web_1.png"
      />
    </aside>
  </main>
</template>

<script>
import { useStore } from "@/store";
export default {
  name: "ChocoIndex",
  setup() {
    const store = useStore();

    const initPage = async () => {
      store.isLoading = true;
      await store.getFoodRestList();
      await store.getFoodCategories();
      store.isLoading = false;
    };

    initPage();
  },
};
</script>
