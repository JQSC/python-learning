const fs = require('fs');
const path = require('path');

// 读取文件
const readFileSync = (filePath) => {
	try {
		return fs.readFileSync(filePath, 'utf8');
	} catch (err) {
		console.error(err);
		return null;
	}
};

// 写入文件
const writeFileSync = (filePath, content) => {
	try {
		fs.writeFileSync(filePath, content, 'utf8');
	} catch (err) {
		console.error(err);
	}
};

// 将类名转换为小驼峰形式
const camelCaseClassName = (className) => {
	return className.replace(/[-_]([a-z])/g, (match, char) => char.toUpperCase());
};

// 转换 less 样式文件
const transformLess = (filePath) => {
	const fileContent = readFileSync(filePath);
	if (!fileContent) return;

	const replacedCss = fileContent.replace(
		/([.#])([\w-]+)/g,
		(match, prefix, className) => {
			if (!className.includes('ant')) {
				return `${prefix}${camelCaseClassName(className)}`;
			} else {
				return match;
			}
		}
	);

	const outputFilePath = filePath.replace('.less', '.module.less');
	writeFileSync(outputFilePath, replacedCss);
	console.log(`Transformed LESS file: ${filePath} -> ${filePath}`);
};

// 转换 React 代码文件
const transformReact = (filePath) => {
	const fileContent = readFileSync(filePath);
	if (!fileContent) return;

	const transformedCode = fileContent.replace(
		/className="([^"]*)"/g,
		(match, className) => {
			return `className={styles.${camelCaseClassName(className)}}`;
		}
	);

	const transformedCode2 = transformedCode.replace(
		/import "\.\/index\.less"/g,
		(match, importContent) => {
			return `import styles from './index.module.less'`;
		}
	);

	// const outputFilePath = filePath.replace('.tsx', '.transformed.tsx');
	writeFileSync(filePath, transformedCode2);
	console.log(`Transformed React file: ${filePath} -> ${filePath}`);
};

// 处理文件
const processFile = (filePath) => {
	console.log('filePath', filePath);
	if (filePath.endsWith('.less')) {
		console.log('less');
		transformLess(filePath);
	} else if (filePath.endsWith('.tsx')) {
		console.log('tsx');
		transformReact(filePath);
	}
};

const readDirectory = (dir, excludeExtensions = []) => {
	let results = [];

	const list = fs.readdirSync(dir);
	list.forEach((file) => {
		file = path.resolve(dir, file);
		const stat = fs.statSync(file);
		if (stat && stat.isDirectory()) {
			// 递归读取子目录
			results = results.concat(readDirectory(file, excludeExtensions));
		} else {
			// 获取文件扩展名
			const ext = path.extname(file);
			// 如果文件扩展名不在剔除列表中，则添加文件路径到结果数组
			if (excludeExtensions.includes(ext)) {
				results.push(file);
			}
		}
	});

	return results;
};

// 入口函数
const main = (filePath) => {
	// const filePath = path.join(process.cwd(), './文件格式化/EjobCorrection.tsx');
	if (!filePath) {
		console.error('Please provide a file path.');
		return;
	}
	processFile(filePath);
};

// main();

const projectPath = '';
const directoryPath = path.join(process.cwd(), projectPath);
const filePaths = readDirectory(directoryPath, ['.less']);
console.log('filePaths', filePaths);
filePaths.forEach((filePath) => {
	main(filePath);
});
