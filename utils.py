import numpy as np
import PIL
from PIL import Image, ImageFilter
import io

def img_to_bytes(img):
    '''
    img to bytes for viewing
    '''
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()




def grayscale(img):
    '''
    rgb2gray using simple mean
    '''
    img = np.array(img)
    out = img.mean(axis=2)
    out = out.astype('uint8')
    return out

def load_image(file_path, target, im_size):
    '''
    Given img path, img window, reads, resizes, transforms to bytes and displays window
    '''
    img = Image.open(file_path).resize((im_size, im_size))
    data = img_to_bytes(img)
    target.update(data = data)
    return img

def nakladanie(img1, img2, rescale):
    # funkcja w opencv
    # img = cv2.addWeighted(img1, rescale, img2, 1-rescale, 0)
    img1 = np.array(img1)
    img2 = np.array(img2)
    img = np.zeros(img1.shape, dtype='float16')
    img = (img1*rescale + img2*(1-rescale)).astype('uint8')
    return img

def binarize(img, threshold=127):
    '''
    binarization
    '''
    img = np.array(img)
    gray = grayscale(img)
    gray[gray>=threshold] = 255
    gray[gray<threshold] = 0

    return gray


def niblack(img, n, k):
    '''binaryzacja niblacka
    n = kernel size defined by the number of neighbours
    1 -> 3x3, 2 -> 5x5'''
    img = np.array(img)
    n = int(n)
    h, w = img.shape[:2]
    # original grayscale
    gray_temp = grayscale(img)
    # grayscale with a n size border of black pixels 
    gray = np.zeros((h+2*n, w+2*n))
    gray[n:-n, n:-n] = gray_temp
    out = np.zeros_like(gray_temp)

    for i in range(n, h-n):
        for j in range(n, w-n):
            # current kernel
            roi = gray[i-n:i+n+1, j-n:j+n+1]
            # thresholding for this kernel
            T = roi.mean() -k*roi.std()
            out[i, j] = 0 if gray[i, j] < T else 255
    
    return out


def sauvola(img, n, k, r):
    '''
    img, n - size of kernel, k - strength of thresholding, R - scaling
    '''
    img = np.array(img)
    n = int(n)
    h, w = img.shape[:2]
    # original grayscale
    gray_temp = grayscale(img)
    # grayscale with a n size border of black pixels 
    gray = np.zeros((h+2*n, w+2*n))
    gray[n:-n, n:-n] = gray_temp
    out = np.zeros_like(gray_temp)

    for i in range(n, h-n):
        for j in range(n, w-n):
            # current kernel
            roi = gray[i-n:i+n+1, j-n:j+n+1]
            # thresholding for this kernel
            T = roi.mean()*(1 -k*(1 - roi.std()/r))
            out[i, j] = 0 if gray[i, j] < T else 255
    
    return out


def rid_calvard(img):
    '''
    Automaticaly finds thresholding value by assuming corner of image as image background
    Then iteratively computes new threshold by comparing means of regions where thresholding is applied
    '''
    # original grayscale
    img = np.array(img)
    gray = grayscale(img)
    out = np.zeros_like(gray)

    # corner size
    cor_size = 150
    ## Initial thresholding value calculation
    # threshold bg = 4 corners
    t_bg1 = gray[:cor_size, :cor_size]   # UL
    t_bg2 = gray[:cor_size:, -cor_size:] # UR
    t_bg3 = gray[-cor_size:, :cor_size]  # DL
    t_bg4 = gray[-cor_size:, -cor_size:] # DR
    t_bg = np.concatenate([t_bg1, t_bg2, t_bg3, t_bg4])
    # threshold foreground
    t_fg1 = gray[:cor_size,  cor_size:-cor_size]    # UP
    t_fg2 = gray[-cor_size:, cor_size:-cor_size]    # DOWN
    t_fg3 = gray[cor_size:-cor_size,:]              # Middle
    t_fg = np.concatenate([t_fg1.flatten(), t_fg2.flatten(), t_fg3.flatten()])
    # threshold value
    threshold_zero = (t_bg.mean() + t_fg.mean())/2

    # generating new thresholding value
    while True:
        # pixels above threshold
        t1_above = gray[gray >= threshold_zero]
        # pixels below threshold
        t1_below = gray[gray < threshold_zero]
        # new threshold
        threshold_one = (t1_above.mean() + t1_below.mean())/2

        # while threshold changes update, else break
        if threshold_one != threshold_zero:
            threshold_zero = threshold_one
        else:
            break
    
    out[gray>=threshold_zero] = 255
    out[gray<threshold_zero] = 0
            
    return out


def otsu(img):
    # original grayscale
    img = np.array(img)
    gray = grayscale(img)
    
    war_within = np.zeros(gray.max())

    for t in range(0, war_within.shape[0]):
        out = np.zeros_like(gray)
        out[gray > t] = 1

        # compute weights
        weight_total = out.size
        non_zero_pixels = out[out == 1].size
        weight_fg = non_zero_pixels/weight_total
        weight_bg = 1-weight_fg
        
        # if all one color then next
        if weight_fg == 0 or weight_bg ==0:
            war_within[t] = np.inf

        # pixele danej klasyna oryginale
        val_pixels_fg = gray[out == 1]
        val_pixels_bg = gray[out == 0]

        # variance
        var_fg = np.var(val_pixels_fg) if len(val_pixels_fg) > 0 else 0 
        var_bg = np.var(val_pixels_bg) if len(val_pixels_bg) > 0 else 0 
        # score
        war_within[t] = weight_fg*var_fg + weight_bg*var_bg

    # selection of best
    best_th = np.argmin(war_within)    
    return binarize(img, best_th)


def combine_img_mask(img, mask):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)
    if isinstance(mask, np.ndarray):
        mask = Image.fromarray(mask)
    black = Image.fromarray(np.zeros_like(img, 'uint8'))
    return Image.composite(img, black, mask)

def erode(cycles, img):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)
    for _ in range(cycles):
        img = img.filter(ImageFilter.MinFilter(3))
    return img


def dilate(cycles, img):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)
    for _ in range(cycles):
         img = img.filter(ImageFilter.MaxFilter(3))
    return img

def convolution(img, kernel):
    img = np.array(img)
    img = grayscale(img)
    h, w = img.shape[:2]
    out = np.zeros((h, w), dtype='uint8')
    
    # (5x5) kernel, n_neigh = 2
    n_neigh = kernel.shape[0]//2
    # extended version of img for kernel processing (254x254) for kernel on outer areas
    img_extnd = np.zeros((h+2*n_neigh, w+2*n_neigh), dtype=np.float16)
    img_extnd[n_neigh:h+n_neigh, n_neigh:w+n_neigh] = img
    # cropping type option?
    
    ## convolution
    # iterating over image area in extended image version
    rows, cols = img_extnd.shape
    for i in range(n_neigh,rows-n_neigh):
        for j in range(n_neigh, cols-n_neigh):
            # convolution in ROI, sum of matched pixels multiplications
            pixel_val = np.einsum('ij, ij ->',
                                    img_extnd[i-n_neigh:i+n_neigh+1, j-n_neigh:j+n_neigh+1],
                                    kernel)
            # fixing potential overflow
            pixel_val = 255 if pixel_val>255 else int(pixel_val)

            out[i-n_neigh, j-n_neigh] = pixel_val
    return out


def gaussianKernel(kernel_size, sigma=1.):
    ax = np.linspace(-(kernel_size-1)/2., (kernel_size-1)/2., kernel_size)
    gauss = np.exp(-0.5*ax**2/np.sqrt(sigma))
    kernel = np.outer(gauss, gauss)
    return kernel/np.sum(kernel)


if __name__ == '__main__':
    np.random.seed(10)
    img = np.random.randint(0, 255, (50, 50, 3))
    #otsu(img)
    ker = np.ones((3, 3))/9
    xd = convolution(img, ker)
    print(xd.shape)
    
