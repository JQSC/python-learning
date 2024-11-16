import { getSafetyAgreement } from '@common/js/safetyAgreement';
import { Form, FormInstance, Checkbox } from 'antd';
import React from 'react';

/**
 * AgreenChecked 组件，用于渲染并检查用户是否勾选了增值服务协议的复选框
 * @param {Object} props - 组件的属性对象
 * @param {FormInstance} props.form - antd Form 组件实例，用于表单数据的收集和校验
 * @returns {JSX.Element} - 返回渲染后的表单组件，其中包含一个复选框用于用户接受协议
 */
const AgreenChecked = (props: { form: FormInstance }) => {
  return (
    <Form form={props.form}>
      <Form.Item
        style={{ marginBottom: 0 }}
        name="agreen"
        valuePropName="checked"
        initialValue={true}
        rules={[
          {
            validator: (rule, value) => {
              if (!value) {
                return Promise.reject(new Error('请勾选协议'));
              } else return Promise.resolve();
            }
          }
        ]}
      >
        <Checkbox>
          <span style={{ color: 'var(--teno-text-color-tertiary)' }}>
            接受
            <a href={getSafetyAgreement('A0035')} target="_blank">
              《猎聘增值服务协议（猎头端）》
            </a>
          </span>
        </Checkbox>
      </Form.Item>
    </Form>
  );
};

export default AgreenChecked;