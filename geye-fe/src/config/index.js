const config = {
  BASE_API: process.env.NODE_ENV === "production" ? "http://example.com" : "http://192.168.62.129:8080",
};

export default config;
