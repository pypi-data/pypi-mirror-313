from setuptools import setup, find_packages
		    
setup(						
    name="iloveyoupain",         
    version="0.3.0",                    # نسخه کتابخانه
    author="ehgehgheighe",                       # نویسنده
    description="a simple code",        # توضیحات کوتاه
    long_description=open("README.md").read(),  # توضیحات بلند
    long_description_content_type="text/markdown",
    packages=find_packages(),          # پیدا کردن ماژول‌ها
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
