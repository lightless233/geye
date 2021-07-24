const path = require("path")

module.exports = {
    publicPath: "/public",
    outputDir: path.join(__dirname, "../templates/"),
    lintOnSave: false,
};
