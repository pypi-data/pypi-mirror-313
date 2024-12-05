// Web storage API

// localStorage用的较多，所以在创建和获取的时候默认为storage，如果是用sessionStorage请传另一个参数flag为false

export const getStorage = (key: string, flag = true): string | null => {
  return flag ? localStorage.getItem(key) : sessionStorage.getItem(key);
};

export const setStorage = (key: string, value: string, flag = true) => {
  flag ? localStorage.setItem(key, value) : sessionStorage.setItem(key, value);
};

export const removeStorage = (key: string, flag = true) => {
  flag ? localStorage.removeItem(key) : sessionStorage.removeItem(key);
};

export const clearStorage = (flag = true) => {
  flag ? localStorage.clear() : sessionStorage.clear();
};
