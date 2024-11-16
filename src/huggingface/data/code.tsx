import { getSafetyAgreement } from "@common/js/safetyAgreement";
import { Form, FormInstance, Checkbox } from "antd";
import React from "react";
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
                return Promise.reject(new Error("请勾选协议"));
              } else return Promise.resolve();
            },
          },
        ]}
      >
        <Checkbox>
          <span style={{ color: "var(--teno-text-color-tertiary)" }}>
            接受
            <a href={getSafetyAgreement("A0035")} target="_blank">
              《猎聘增值服务协议（猎头端）》
            </a>
          </span>
        </Checkbox>
      </Form.Item>
    </Form>
  );
};
export default AgreenChecked;
