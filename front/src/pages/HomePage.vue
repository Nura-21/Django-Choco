<template>
  <section class="page home">
    <aside class="home-link">
      <router-link :to="{ name: 'chocofood' }">
        <img :src="$getImage('img/chocofood-full.png')" draggable="false" />
      </router-link>
    </aside>
    <aside class="home-link">
      <router-link :to="{ name: 'chocolife' }">
        <img :src="$getImage('img/chocolife-full.jpeg')" draggable="false" />
      </router-link>
    </aside>
  </section>
</template>

<script setup></script>