import { combineReducers } from "redux";
import auth from "./auth";
import quiz_editor from "./quiz_editor";

export default combineReducers({
    auth,
    quiz_editor
});