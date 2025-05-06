const { createApp } = Vue;

createApp({
  data() {
    return {
      searchQuery: "",
      results: [],
      loading: false,
      error: ""
    };
  },
  methods: {
    async searchMovie() {
      if (!this.searchQuery.trim()) return;

      this.loading = true;
      this.error = "";
      this.results = [];

      try {
        const response = await fetch(`/movies/?title=${encodeURIComponent(this.searchQuery)}`);
        if (!response.ok) {
          throw new Error("No movies found.");
        }
        this.results = await response.json();
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    }
  }
}).mount("#app");
