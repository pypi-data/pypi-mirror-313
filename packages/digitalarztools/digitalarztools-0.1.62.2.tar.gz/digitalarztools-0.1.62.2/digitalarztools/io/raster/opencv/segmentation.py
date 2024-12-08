import cv2
import numpy as np
import matplotlib.pyplot as plt

from digitalarztools.raster.rio_process import RioProcess
from digitalarztools.raster.rio_raster import RioRaster


class CVSegmentation:
    raster: RioRaster

    def __init__(self, raster: RioRaster):
        self.raster = raster

    @staticmethod
    def plot_img(img, title):
        plt.imshow(img)
        plt.axis("off")
        plt.title(title)
        plt.show()

    def calculate_region_using_contour(self, band: tuple):
        data = RioProcess.min_max_stretch(self.raster, band)
        data = np.moveaxis(data, 0, 2)
        img1, img2 = self.region_detection_using_contour(data)
        img1 = np.moveaxis(img1, 2, 0)
        img2 = np.moveaxis(img2, 2, 0)

        classified_raster1 = RioRaster.raster_from_array(img1,
                                                         crs=self.raster.get_crs(),
                                                         g_transform=self.raster.get_geo_transform())
        classified_raster2 = RioRaster.raster_from_array(img2,
                                                         crs=self.raster.get_crs(),
                                                         g_transform=self.raster.get_geo_transform())
        return classified_raster1, classified_raster2

    def calculate_k_mean_cluster(self, k: int) -> RioRaster:
        """
        :param k: no of classes
        :return:
        """
        data = self.raster.get_data_array(band=(1, 2, 3))
        data = np.moveaxis(data, 0, 2)
        segmented_image, labels = self.k_mean_clustering(data, k)
        # print(segmented_image.shape)
        # print(labels.shape)
        labels = np.expand_dims(labels, axis=2)
        classified_data = np.concatenate((segmented_image, labels), axis=2)
        classified_data = np.moveaxis(classified_data, 2, 0)
        print(classified_data.shape)
        classified_raster = RioRaster.raster_from_array(classified_data,
                                                        crs=self.raster.get_crs(),
                                                        g_transform=self.raster.get_geo_transform())
        return classified_raster

    @classmethod
    def test_k_mean_clustering(cls):
        image = cv2.imread("test_data/image.jpg")
        # convert to RGB
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        segmented_image, labels = cls.k_mean_clustering(image, k=3)
        # show the image
        plt.imshow(segmented_image)
        plt.show()
        plt.imshow(labels)
        plt.show()

    # @staticmethod
    # def mask_image_class(image: np.ndarray, class_label):
    #     # disable only the cluster number 2 (turn the pixel into black)
    #     masked_image = np.copy(image)
    #     # convert to the shape of a vector of pixel values
    #     masked_image = masked_image.reshape((-1, 3))
    #     # color (i.e cluster) to disable
    #     masked_image[labels == class_label] = [0, 0, 0]
    #     # convert back to original shape
    #     masked_image = masked_image.reshape(image.shape)
    #     # show the image
    #     plt.imshow(masked_image)
    #     plt.show()
    @staticmethod
    def k_mean_clustering(image: np.ndarray, k: int) -> (np.ndarray, np.ndarray):
        """
        :param image: BGR/RGB image with row, cols, band form
        :param k: no of classes
        :return:
        """
        # reshape the image to a 2D array of pixels and 3 color values (RGB)
        pixel_values = image.reshape((-1, 3))
        # convert to float
        pixel_values = np.float32(pixel_values)
        print(pixel_values.shape)
        """
        define stopping criteria 
        default is 3 min
        stop either when some number of iterations is exceeded (say 100), 
        or if the clusters move less than some epsilon value (let's pick 0.2 here)
        """
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

        """
        number of clusters (K)
        cv2.KMEANS_RANDOM_CENTERS just indicates OpenCV to randomly assign the values of the clusters initially.
        """
        _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # convert back to 8 bit values
        centers = np.uint8(centers)
        # centers = np.uint8(np.arange(len(centers)))

        # flatten the labels array
        labels = labels.flatten()

        # convert all pixels to the color of the centroids
        segmented_image = centers[labels.flatten()]

        # reshape back to the original image dimension
        segmented_image = segmented_image.reshape(image.shape)
        *_, bands = image.shape
        labels = labels.reshape(*_)

        return segmented_image, labels

    @staticmethod
    def test_edge_detection():
        img = cv2.imread("test_data/image.jpg")
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    @staticmethod
    def edge_detection():
        img = cv2.imread("test_data/image.jpg")
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # converting to grayscale image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Blurring the image using 3x3
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # Canny Edge detection
        for idx, i in enumerate(range(10, 150, 25)):
            edged = cv2.Canny(gray, idx, 200)

    @classmethod
    def test_region_detection_using_contour(cls):
        image1 = cv2.imread('test/image_2.jpg')
        cls.region_detection_using_contour(image1)

    @classmethod
    def region_detection_using_contour(cls, image1: np.ndarray):
        """
        https://learnopencv.com/contour-detection-using-opencv-python-c/
        :param image1:
        :return:
        """
        row, col, band = image1.shape
        img_gray1 = image1 if band == 1 else cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        # ret, thresh1 = cv2.threshold(img_gray1, 150, 255, cv2.THRESH_BINARY)
        contours2, hierarchy2 = cv2.findContours(img_gray1, cv2.RETR_TREE,
                                                 cv2.CHAIN_APPROX_SIMPLE)
        image_copy2 = np.zeros(image1.shape)
        cv2.drawContours(image_copy2, contours2, -1, 8, 2, cv2.LINE_AA)
        image_copy3 = np.zeros(image1.shape)
        for i, contour in enumerate(contours2):  # loop over one contour area
            for j, contour_point in enumerate(contour):  # loop over the points
                # draw a circle on the current contour coordinate
                cv2.circle(image_copy3, ((contour_point[0][0], contour_point[0][1])), 2, 8, 2, cv2.LINE_AA)
        # cls.plot_img(image_copy2, "image1")
        cls.plot_img(image_copy3, "image2")
        return image_copy2, image_copy3


if __name__ == "__main__":
    # CVSegmentation.test_k_mean_clustering()
    CVSegmentation.test_region_detection_using_contour()
