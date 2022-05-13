import mongoose from "mongoose";
mongoose.connect("mongodb://127.0.0.1:27017/worldexb", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const db = mongoose.connection;
const handleOpen = () => console.log("🟢 Database 연결");
const handleError = (err) => console.log("🔺 Database 에러", err);

db.on("error", handleError);
db.once("open", handleOpen);