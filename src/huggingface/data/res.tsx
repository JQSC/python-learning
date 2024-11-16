/**
 * AgreenChecked 组件，用于在表单中渲染一个协议接受的复选框
 * @param {Object} props - 组件的属性对象
 * @param {FormInstance} props.form - form schema class 的实例
 * @returns {JSX.Element} - 返回包含协议接受复选框的表单组件
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