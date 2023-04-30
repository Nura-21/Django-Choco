<template>
  <footer v-if="$store.hasLogged" class="footer food-main-footer">
    <section class="food-main-footer-container">
      <div class="food-main-footer-logo">
        <router-link :to="{ name: 'chocofood' }">
          <img
            draggable="false"
            src="https://chocofood.kz/images/chocofood-w.svg"
          />
        </router-link>
      </div>
      <div class="food-main-footer-nav">
        <aside v-for="(optionList, index) of navOptions" :key="index">
          <span v-for="(nav, index) of optionList" :key="nav">
            <b v-if="index === 0">{{ nav }}</b>
            {{ index !== 0 ? nav : null }}
          </span>
        </aside>
      </div>
    </section>
  </footer>
  <footer v-if="$store.hasLogged === false" class="footer food-footer">
    <section class="footer-container">
      <span>© 2013–2022 TОО «Интернет Доставка».</span>
    </section>
  </footer>
</template>

<script>
export default {
  name: "FoodFooter",
  setup() {
    const navOptions = [
      [
        "Партнерам",
        "О компании",
        "Что предлагаем",
        "Откуда клиенты",
        "Как это работает",
        "Соглашение",
        "Карта сайта",
      ],
      ["Мобильное приложение", "Apple Store", "Google Play Market"],
      ["Присоединяйтесь к нам", "Facebook", "ВКонтакте", "Instagram"],
    ];

    return {
      navOptions,
    };
  },
};
</script>
