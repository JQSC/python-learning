export function isHtml(html: string): boolean {
  return /<([A-Za-z][A-Za-z0-9]*)\b[^>]*>(.*?)<\/\1>/.test(html);
}
