import mongoose from "mongoose";

const exbSchema = new mongoose.Schema({
  title: String,
  date: String,
  thumbnailSrc: String,
  detail: String,
  link: String,
});

const ExbModel = mongoose.model("ExbModel", exbSchema);
export default ExbModel;
