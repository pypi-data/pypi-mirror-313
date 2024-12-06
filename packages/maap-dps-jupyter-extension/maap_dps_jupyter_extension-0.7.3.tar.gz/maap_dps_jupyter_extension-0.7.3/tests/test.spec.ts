import { expect, test } from '@jupyterlab/galata';

test('extension activates', async ({ page }) => {
  const logs: string[] = [];

  page.on('console', message => {
    logs.push(message.text());
  });

  await page.goto('http://localhost:8888/lab');

  expect(
    logs.filter(s => s === "JupyterLab MAAP View Jobs extension is activated!")
  ).toHaveLength(1);

  expect(
    logs.filter(s => s === "JupyterLab MAAP Submit Jobs plugin is activated!")
  ).toHaveLength(1);
});
