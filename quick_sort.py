def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2] # 选取中间元素作为基准值
    left = [x for x in arr if x < pivot] # 小于基准值的部分放在左边列表
    middle = [x for x in arr if x == pivot] # 等于基准值的部分放在中间列表
    right = [x for x in arr if x > pivot] # 大于基准值的部分放在右边列表
    
    return quick_sort(left) + middle + quick_sort(right) # 递归调用对左、中、右三个子数组进行排序并合并结果

# 测试样例
array = [5, 3, 8, 4, 6, 7, 9, 2, 1, 0]
sorted_array = quick_sort(array)
print("排序后的数组：", sorted_array)
