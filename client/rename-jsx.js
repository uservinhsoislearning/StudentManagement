// rename-jsx.js
import fs from "fs";
import path from "path";

const walkDir = (dir, callback) => {
  fs.readdirSync(dir).forEach((f) => {
    const dirPath = path.join(dir, f);
    const isDirectory = fs.statSync(dirPath).isDirectory();
    isDirectory ? walkDir(dirPath, callback) : callback(path.join(dir, f));
  });
};

const containsJSX = (content) => {
  return /<[^>]+>/.test(content) && /return\s*\(.*</s.test(content);
};

const targetDir = "./src";

walkDir(targetDir, (filePath) => {
  if (filePath.endsWith(".js")) {
    const content = fs.readFileSync(filePath, "utf8");

    if (containsJSX(content)) {
      const newPath = filePath.replace(/\.js$/, ".jsx");
      fs.renameSync(filePath, newPath);
      console.log(`✅ Renamed: ${filePath} → ${newPath}`);
    }
  }
});
