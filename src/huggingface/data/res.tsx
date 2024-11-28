```javascript
import { getSafetyAgreement } from "@common/js/safetyAgreement";
import styles from "./index.module.less"; // style
import { utils } from "./utils";
import { Form, FormInstance, Checkbox } from "antd";
import React, { CSSProperties } from "react";

/**
 * 企业Logo组件的属性接口
 * @interface LogoProps
 * @property {string} src - logo图片地址
 * @property {number} [size=48] - logo尺寸大小
 * @property {CSSProperties} [style] - 自定义样式
 */
interface LogoProps {
  /** logo地址 */
  src: string;
  /**
   * logo尺寸
   * @default 48
   */
  size?: number;
  /** 附加样式 */
  style?: CSSProperties;
}

/**
 * CompanyLogo 组件，用于显示企业Logo
 * @param {LogoProps} props - 组件的属性对象
 * @param {string} props.src - logo图片地址
 * @param {number} [props.size=48] - logo尺寸大小
 * @param {CSSProperties} [props.style] - 自定义样式
 * @returns {JSX.Element} - 返回企业Logo的JSX元素
 */
const CompanyLogo = ({ src, style, size = 48 }: LogoProps) => (
  <p
    className={styles.companyLogo}
    style={{ width: size, height: size, ...style }}
  >
    <img src={src} alt="logo" />
  </p>
);

export default CompanyLogo;
```